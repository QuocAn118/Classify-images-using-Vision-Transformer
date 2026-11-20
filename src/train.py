"""TASK-006: train ViT/CNN, quick và resume; chỉ đọc train/validation."""
from __future__ import annotations

import argparse
from copy import deepcopy
import csv
import io
from itertools import islice
import json
import math
import os
from pathlib import Path
import random
import re
import tempfile
import time

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from src.data import build_loader
from src.models import build_model
from src.utils import atomic_save, load_config, make_run_name, set_seed

LOG_FIELDS = ("epoch", "train_loss", "train_acc", "val_loss", "val_top1", "val_top5", "lr", "epoch_time_s")


def validate_config(cfg: dict) -> None:
    """Từ chối cấu hình gây sai lịch train hoặc ghi file ra ngoài outputs."""
    if not isinstance(cfg["run_name"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", cfg["run_name"]):
        raise ValueError("run_name chỉ được chứa chữ, số, _, - và dấu chấm")
    for key, value in (("epochs", cfg["train"]["epochs"]), ("batch_size", cfg["data"]["batch_size"]),
                       ("num_classes", cfg["data"]["num_classes"]), ("img_size", cfg["data"]["img_size"])):
        if type(value) is not int or value <= 0:
            raise ValueError(f"{key} phải là số nguyên dương")
    if type(cfg["seed"]) is not int or not 0 <= cfg["seed"] < 2**32:
        raise ValueError("seed phải là số nguyên thuộc [0, 2**32)")
    t = cfg["train"]
    if not isinstance(t["optimizer"], str) or t["optimizer"].lower() != "adamw":
        raise ValueError("So sánh chính chỉ hỗ trợ optimizer adamw")
    for key in ("lr", "weight_decay", "warmup_epochs", "min_lr", "label_smoothing",
                "grad_clip", "mixup_alpha", "cutmix_alpha", "mix_prob"):
        value = t[key]
        if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f"train.{key} phải hữu hạn và không âm")
    if t["lr"] == 0 or t["grad_clip"] == 0 or t["min_lr"] > t["lr"]:
        raise ValueError("lr, grad_clip phải dương và min_lr không vượt lr")
    if not 0 <= t["mix_prob"] <= 1 or not 0 <= t["label_smoothing"] < 1:
        raise ValueError("mix_prob phải thuộc [0,1], label_smoothing thuộc [0,1)")
    if not isinstance(t["amp"], bool):
        raise ValueError("train.amp phải là true hoặc false")


def build_optimizer(model: nn.Module, cfg: dict) -> torch.optim.Optimizer:
    """Bias, normalization và CLS/positional embedding không chịu weight decay."""
    decay, no_decay = [], []
    for name, param in model.named_parameters():
        if param.requires_grad:
            group = no_decay if param.ndim <= 1 or name.endswith(("cls_token", "pos_embed")) else decay
            group.append(param)
    return torch.optim.AdamW(
        [{"params": decay, "weight_decay": cfg["train"]["weight_decay"]},
         {"params": no_decay, "weight_decay": 0.0}], lr=cfg["train"]["lr"],
    )


def build_scheduler(optimizer: torch.optim.Optimizer, cfg: dict, steps_per_epoch: int):
    """Warmup tuyến tính rồi cosine; bước cuối dùng min_lr."""
    t = cfg["train"]
    total = t["epochs"] * steps_per_epoch
    warmup = min(int(t["warmup_epochs"] * steps_per_epoch), max(0, total - 1))
    floor = t["min_lr"] / t["lr"]

    def factor(step):
        if step < warmup:
            return (step + 1) / warmup
        progress = min(1.0, (step - warmup) / max(1, total - warmup - 1))
        return floor + (1 - floor) * (1 + math.cos(math.pi * progress)) / 2

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, factor)
    scheduler.steps_per_epoch = steps_per_epoch
    return scheduler


def mix_batch(x: torch.Tensor, y: torch.Tensor, cfg: dict) -> tuple[torch.Tensor, torch.Tensor]:
    """Mixup hoặc CutMix, nhãn mềm dùng đúng diện tích hộp đã cắt."""
    t = cfg["train"]
    modes = [mode for mode in ("mixup", "cutmix") if t[f"{mode}_alpha"] > 0]
    if not modes or torch.rand(()).item() >= t["mix_prob"]:
        return x, y
    mode = random.choice(modes)
    lam = float(np.random.beta(t[f"{mode}_alpha"], t[f"{mode}_alpha"]))
    order = torch.randperm(len(y), device=x.device)
    soft = nn.functional.one_hot(y, cfg["data"]["num_classes"]).to(x.dtype)
    if mode == "mixup":
        x = lam * x + (1 - lam) * x[order]
    else:
        h, w = x.shape[-2:]
        cut_h, cut_w = int(h * math.sqrt(1 - lam)), int(w * math.sqrt(1 - lam))
        cy, cx = int(torch.randint(h, ()).item()), int(torch.randint(w, ()).item())
        y1, y2 = max(0, cy - cut_h // 2), min(h, cy + (cut_h + 1) // 2)
        x1, x2 = max(0, cx - cut_w // 2), min(w, cx + (cut_w + 1) // 2)
        x = x.clone()
        x[:, :, y1:y2, x1:x2] = x[order, :, y1:y2, x1:x2]
        lam = 1 - (y2 - y1) * (x2 - x1) / (h * w)
    return x, lam * soft + (1 - lam) * soft[order]


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
        os.replace(name, path)
    except BaseException:
        Path(name).unlink(missing_ok=True)
        raise


def save_log(history: list[dict], path: Path) -> None:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=LOG_FIELDS)
    writer.writeheader()
    writer.writerows(history)
    _atomic_write(path, stream.getvalue().encode("utf-8"))


def plot_curves(history: list[dict], path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    epochs = [r["epoch"] for r in history]
    for key in ("train_loss", "val_loss"):
        axes[0].plot(epochs, [r[key] for r in history], label=key)
    for key in ("val_top1", "val_top5"):
        axes[1].plot(epochs, [r[key] for r in history], label=key)
    for ax in axes:
        ax.set_xlabel("Epoch")
        ax.legend()
    axes[0].set_ylabel("Cross entropy")
    axes[1].set_ylabel("Accuracy (%)")
    fig.tight_layout()
    stream = io.BytesIO()
    fig.savefig(stream, format="png", dpi=120)
    plt.close(fig)
    _atomic_write(path, stream.getvalue())


def _loaders(cfg: dict, quick: bool) -> tuple[DataLoader, DataLoader, bool]:
    d = cfg["data"]
    cache = Path(d["cache_dir"])
    missing = any(not (cache / f"{split}_{kind}.npy").is_file()
                  for split in ("train", "val") for kind in ("x", "y"))
    if quick and missing:
        print("CẢNH BÁO: thiếu cache train/val; --quick dùng dữ liệu giả, không phải kết quả huấn luyện thật.", flush=True)
        generator = torch.Generator().manual_seed(cfg["seed"])
        loaders = []
        for _ in range(2):
            n = 2 * d["batch_size"]
            x = torch.randn(n, 3, d["img_size"], d["img_size"], generator=generator)
            y = torch.randint(d["num_classes"], (n,), generator=generator)
            loaders.append(DataLoader(TensorDataset(x, y), batch_size=d["batch_size"]))
        return *loaders, True
    return build_loader(cfg, "train"), build_loader(cfg, "val"), False


def _rng_state() -> dict:
    numpy_state = np.random.get_state()
    return {"python": random.getstate(), "numpy": (numpy_state[0], numpy_state[1].tolist(), *numpy_state[2:]),
            "torch": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else []}


def _restore_rng(state: dict) -> None:
    random.setstate(state["python"])
    numpy_state = state["numpy"]
    np.random.set_state((numpy_state[0], np.array(numpy_state[1], dtype=np.uint32), *numpy_state[2:]))
    torch.set_rng_state(state["torch"])
    if torch.cuda.is_available() and state["cuda"]:
        torch.cuda.set_rng_state_all(state["cuda"])


def run_epoch(model, loader, criterion, device, cfg, optimizer=None, scheduler=None, scaler=None, limit=None):
    """Loss trung bình theo ảnh, Top-1/5 theo phần trăm; val không bật augmentation batch."""
    training = optimizer is not None
    model.train(training)
    totals = torch.zeros(4, device=device, dtype=torch.float64)
    amp = device.type == "cuda" and cfg["train"]["amp"]
    with torch.set_grad_enabled(training):
        for x, y in islice(loader, limit):
            x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
            if training:
                optimizer.zero_grad(set_to_none=True)
                x, targets = mix_batch(x, y, cfg)
            else:
                targets = y
            with torch.autocast(device_type=device.type, enabled=amp):
                logits = model(x)
                loss = criterion(logits, targets)
            if not torch.isfinite(loss):
                raise FloatingPointError("Loss không hữu hạn; dừng, giữ checkpoint epoch trước")
            if training:
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                nn.utils.clip_grad_norm_(model.parameters(), cfg["train"]["grad_clip"], error_if_nonfinite=not amp)
                previous_scale = scaler.get_scale()
                scaler.step(optimizer)
                scaler.update()
                if scaler.get_scale() >= previous_scale:
                    scheduler.step()
            top = logits.detach().topk(min(5, logits.shape[1]), dim=1).indices
            totals += torch.stack((loss.detach().double() * len(y), (top[:, 0] == y).sum(),
                                   (top == y[:, None]).any(dim=1).sum(), y.new_tensor(len(y))))
    loss_sum, top1, top5, count = totals.tolist()
    if count == 0:
        raise ValueError("DataLoader không có batch; kiểm tra cache và batch_size")
    return loss_sum / count, 100 * top1 / count, 100 * top5 / count


def train(cfg: dict, *, quick: bool = False, resume: str | Path | None = None,
          device: str | None = None, out_dir: str | Path = "outputs") -> dict:
    """Train và trả thông tin bàn giao; không thay đổi config của bên gọi."""
    cfg = deepcopy(cfg)
    cfg["train"] = {"warmup_epochs": 5, "min_lr": 1e-5, "label_smoothing": 0.1,
                    "grad_clip": 1.0, "amp": True, "mixup_alpha": 0.8,
                    "cutmix_alpha": 1.0, "mix_prob": 0.5, **cfg["train"]}
    validate_config(cfg)
    if quick:
        cfg["run_name"] += "_quick"
        cfg["train"]["epochs"] = min(2, cfg["train"]["epochs"])
    set_seed(cfg["seed"])
    device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    if device.type == "cuda" and not torch.cuda.is_available():
        raise ValueError("Đã chọn CUDA nhưng không có GPU CUDA khả dụng")
    name, out = make_run_name(cfg), Path(out_dir)
    last_path, best_path = (out / "checkpoints" / f"{name}_{kind}.pt" for kind in ("last", "best"))
    log_path, curve_path = out / "logs" / f"{name}.csv", out / "figures" / f"{name}_curves.png"
    if not resume and any(path.exists() for path in (last_path, best_path, log_path, curve_path)):
        raise FileExistsError(f"Lần chạy {name} đã tồn tại; dùng --resume hoặc đổi run_name/seed")

    train_loader, val_loader, synthetic = _loaders(cfg, quick)
    steps = min(2, len(train_loader)) if quick else len(train_loader)
    if steps == 0 or len(val_loader) == 0:
        raise ValueError("DataLoader không có batch; kiểm tra cache và batch_size")
    if synthetic:
        class_names = [f"class_{i}" for i in range(cfg["data"]["num_classes"])]
    else:
        names_path = out / "results" / "class_names.json"
        class_names = json.loads(names_path.read_text(encoding="utf-8"))
        if (not isinstance(class_names, list) or len(class_names) != cfg["data"]["num_classes"]
                or not all(isinstance(item, str) for item in class_names)):
            raise ValueError("class_names.json không khớp num_classes; chạy lại prepare_data")

    model = build_model(cfg).to(device)
    optimizer = build_optimizer(model, cfg)
    scheduler = build_scheduler(optimizer, cfg, steps)
    amp = device.type == "cuda" and cfg["train"]["amp"]
    scaler = (torch.amp.GradScaler("cuda", enabled=amp) if hasattr(torch.amp, "GradScaler")
              else torch.cuda.amp.GradScaler(enabled=amp))
    criterion = nn.CrossEntropyLoss(label_smoothing=cfg["train"]["label_smoothing"])
    history, start, best_top1, best_checkpoint = [], 1, -1.0, None
    if resume:
        checkpoint = torch.load(resume, map_location="cpu", weights_only=True)
        saved = checkpoint["config"]
        data_keys = set(cfg["data"]) - {"root", "cache_dir", "num_workers"}
        if (any(saved[key] != cfg[key] for key in ("model", "train", "seed", "run_name"))
                or any(saved["data"][key] != cfg["data"][key] for key in data_keys)
                or checkpoint["class_names"] != class_names
                or checkpoint["scheduler"].get("steps_per_epoch", steps) != steps):
            raise ValueError("Resume phải giữ model, lịch train, batch, seed, nhãn và chế độ quick; chỉ đổi đường dẫn/worker")
        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        scheduler.load_state_dict(checkpoint["scheduler"])
        if checkpoint["scaler"] is not None and amp:
            scaler.load_state_dict(checkpoint["scaler"])
        start, best_top1 = checkpoint["epoch"] + 1, checkpoint["best_val_top1"]
        best_checkpoint = checkpoint.get("best_checkpoint")
        history = checkpoint.get("history", [])
        if not history and log_path.exists():
            with log_path.open(encoding="utf-8", newline="") as stream:
                history = [{key: int(value) if key == "epoch" else float(value) for key, value in row.items()}
                           for row in csv.DictReader(stream) if int(row["epoch"]) < start]
        if best_checkpoint is None and history and history[-1]["val_top1"] == best_top1:
            best_checkpoint = {key: value for key, value in checkpoint.items() if key != "best_checkpoint"}
        if "rng_state" in checkpoint:
            _restore_rng(checkpoint["rng_state"])
        checkpoint["best_checkpoint"] = best_checkpoint
        atomic_save(checkpoint, last_path)
        if best_checkpoint is not None:
            atomic_save(best_checkpoint, best_path)
        save_log(history, log_path)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    print(f"run={name} device={device} synthetic={synthetic} epochs={cfg['train']['epochs']} start={start}", flush=True)

    for epoch in range(start, cfg["train"]["epochs"] + 1):
        begin = time.perf_counter()
        train_loss, train_acc, _ = run_epoch(model, train_loader, criterion, device, cfg,
                                            optimizer, scheduler, scaler, limit=2 if quick else None)
        val_loss, val_top1, val_top5 = run_epoch(model, val_loader, criterion, device, cfg, limit=2 if quick else None)
        row = dict(zip(LOG_FIELDS, (epoch, train_loss, train_acc, val_loss, val_top1, val_top5,
                                   optimizer.param_groups[0]["lr"], time.perf_counter() - begin)))
        history.append(row)
        improved = val_top1 > best_top1
        best_top1 = max(best_top1, val_top1)
        checkpoint = {"model": model.state_dict(), "optimizer": optimizer.state_dict(),
                      "scheduler": scheduler.state_dict(), "scaler": scaler.state_dict() if amp else None,
                      "epoch": epoch, "best_val_top1": best_top1, "config": cfg, "seed": cfg["seed"],
                      "class_names": class_names, "history": history, "rng_state": _rng_state()}
        if improved:
            best_checkpoint = deepcopy(checkpoint)
        checkpoint["best_checkpoint"] = best_checkpoint
        atomic_save(checkpoint, last_path)
        if improved:
            atomic_save(best_checkpoint, best_path)
        save_log(history, log_path)
        plot_curves(history, curve_path)
        print(f"epoch={epoch} train_loss={train_loss:.4f} val_loss={val_loss:.4f} "
              f"val_top1={val_top1:.2f} val_top5={val_top5:.2f} time_s={row['epoch_time_s']:.2f}", flush=True)
    if history and start > cfg["train"]["epochs"]:
        plot_curves(history, curve_path)
    peak = torch.cuda.max_memory_allocated(device) / 1024**2 if device.type == "cuda" else None
    return {"run_name": name, "device": str(device), "synthetic": synthetic,
            "best_val_top1": best_top1, "history": history, "peak_vram_mb": peak,
            "last_checkpoint": str(last_path), "best_checkpoint": str(best_path), "log": str(log_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/vit_small.yaml")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--epochs", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--device", choices=("cpu", "cuda"))
    args = parser.parse_args()
    cfg = load_config(args.config)
    if args.epochs is not None:
        cfg["train"]["epochs"] = args.epochs
    if args.seed is not None:
        cfg["seed"] = args.seed
    try:
        result = train(cfg, quick=args.quick, resume=args.resume, device=args.device)
    except (ValueError, FileNotFoundError, FileExistsError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps({key: value for key, value in result.items() if key != "history"}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
