"""CLS maps và attention rollout từ checkpoint ViT đã chốt (TASK-008).

python -m src.attention --checkpoint outputs/checkpoints/vit_small_seed42_best.pt --split test
Hợp đồng và giới hạn sử dụng test: docs/07_evaluation.md, docs/04_data.md.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np
from PIL import Image
import torch
from torch import Tensor, nn
from torch.nn import functional as F

from src.data import build_loader, build_transform
from src.models import build_model
from src.utils import make_run_name


def _validate_attentions(attns: list[Tensor], img_size: int, patch_size: int) -> int:
    if img_size <= 0 or patch_size <= 0 or img_size % patch_size:
        raise ValueError("img_size phải dương và chia hết cho patch_size dương")
    grid = img_size // patch_size
    if not attns:
        raise ValueError("attention list không được rỗng")
    shape = attns[0].shape
    if len(shape) != 4 or shape[0] < 1 or shape[1] < 1 or shape[-2:] != (grid * grid + 1,) * 2:
        raise ValueError("attention phải có shape (B, heads, N+1, N+1) khớp lưới patch")
    for attn in attns:
        if attn.shape != shape or not torch.isfinite(attn).all() or (attn < 0).any():
            raise ValueError("attention phải cùng shape, hữu hạn và không âm")
    return grid


def _resize_map(patches: Tensor, grid: int, img_size: int) -> Tensor:
    maps = F.interpolate(patches.reshape(-1, 1, grid, grid), size=(img_size, img_size),
                         mode="bilinear", align_corners=False)[:, 0]
    low = maps.amin(dim=(-2, -1), keepdim=True)
    span = maps.amax(dim=(-2, -1), keepdim=True) - low
    return torch.where(span > 0, (maps - low) / span.clamp_min(1e-12), torch.zeros_like(maps))


@torch.no_grad()
def cls_attention_map(attns: list[Tensor], img_size: int, patch_size: int) -> Tensor:
    """CLS → patch của layer cuối, trung bình head; trả map (B,H,W) trong [0,1]."""
    grid = _validate_attentions(attns, img_size, patch_size)
    patches = attns[-1].float().mean(dim=1)[:, 0, 1:]
    return _resize_map(patches, grid, img_size)


@torch.no_grad()
def attention_rollout(attns: list[Tensor], img_size: int, patch_size: int) -> Tensor:
    """R_l = RowNorm(0.5*A_l + 0.5*I) @ R_(l-1), theo thứ tự layer thấp → cao."""
    grid = _validate_attentions(attns, img_size, patch_size)
    batch, _, tokens, _ = attns[0].shape
    identity = torch.eye(tokens, device=attns[0].device, dtype=torch.float32)
    result = identity.expand(batch, -1, -1)
    for attn in attns:
        residual = 0.5 * attn.float().mean(dim=1) + 0.5 * identity
        residual = residual / residual.sum(dim=-1, keepdim=True)
        result = residual @ result
    return _resize_map(result[:, 0, 1:], grid, img_size)


def overlay_heatmap(image: Image.Image, heatmap: Tensor | np.ndarray, alpha: float = 0.5) -> Image.Image:
    """Phủ colormap jet lên ảnh RGB; heatmap phải cùng kích thước ảnh và thuộc [0,1]."""
    from matplotlib import colormaps

    image = image.convert("RGB")
    values = heatmap.detach().float().cpu().numpy() if isinstance(heatmap, Tensor) else np.asarray(heatmap)
    if not 0 <= alpha <= 1 or values.shape != (image.height, image.width):
        raise ValueError("alpha phải thuộc [0,1]; heatmap phải cùng kích thước ảnh")
    if not np.isfinite(values).all() or np.any((values < 0) | (values > 1)):
        raise ValueError("heatmap phải hữu hạn và thuộc [0,1]")
    colors = colormaps["jet"](values)[..., :3] * 255
    mixed = (1 - alpha) * np.asarray(image, dtype=np.float32) + alpha * colors
    return Image.fromarray(np.rint(mixed).clip(0, 255).astype(np.uint8))


@torch.inference_mode()
def explain_image(model: nn.Module, image: Image.Image, cfg: dict) -> dict:
    """Dùng lại mô hình đã nạp cho demo; trả ảnh resize, logits và hai map trên CPU."""
    size = cfg["data"]["img_size"]
    resampling = getattr(Image, "Resampling", Image)  # hỗ trợ cả Pillow 9.0
    image = image.convert("RGB").resize((size, size), resampling.BICUBIC)
    x = torch.from_numpy(np.array(image)).permute(2, 0, 1)
    x = build_transform(cfg, train=False)(x).unsqueeze(0)
    model.eval()
    logits, attns = model(x.to(next(model.parameters()).device), return_attn=True)
    patch = cfg["model"]["patch_size"]
    return {"image": image, "logits": logits[0].float().cpu(),
            "cls_map": cls_attention_map(attns, size, patch)[0].cpu(),
            "rollout_map": attention_rollout(attns, size, patch)[0].cpu()}


def load_vit_checkpoint(path: str | Path, device: str = "cpu", expected_sha256: str | None = None) -> tuple[nn.Module, dict]:
    """Nạp strict/weights_only; config và class_names luôn lấy từ chính checkpoint."""
    path = Path(path)
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    sha = digest.hexdigest()
    if expected_sha256 is not None and sha != expected_sha256.lower():
        raise ValueError(f"SHA-256 checkpoint không khớp: {sha}")
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(checkpoint, dict) or not all(k in checkpoint for k in ("config", "model", "class_names")):
        raise ValueError("checkpoint thiếu model/config/class_names theo hợp đồng")
    cfg, names = checkpoint["config"], checkpoint["class_names"]
    if cfg["model"]["name"] != "vit":
        raise ValueError("attention chỉ hỗ trợ checkpoint ViT")
    if (not isinstance(names, list) or len(names) != cfg["data"]["num_classes"]
            or not all(isinstance(name, str) and name for name in names)):
        raise ValueError("class_names không khớp số lớp trong checkpoint")
    mean, std = np.asarray(cfg["data"]["mean"]), np.asarray(cfg["data"]["std"])
    if mean.shape != (3,) or std.shape != (3,) or not np.isfinite(mean).all() or not np.isfinite(std).all() or (std <= 0).any():
        raise ValueError("mean/std phải gồm 3 số hữu hạn, std dương")
    if device == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA không có trên máy này; dùng --device cpu")
    model = build_model(cfg)
    model.load_state_dict(checkpoint["model"], strict=True)
    model.to(device).eval()
    metadata = {"path": path.as_posix(), "sha256": sha, "config": deepcopy(cfg),
                "class_names": names, "epoch": checkpoint.get("epoch"),
                "seed": checkpoint.get("seed", cfg.get("seed")),
                "best_val_top1": checkpoint.get("best_val_top1")}
    return model, metadata


def select_examples(records: list[dict], num_images: int) -> list[dict]:
    """Cân bằng đúng/sai, ưu tiên lớp mới; thứ tự records do seed của lượt scan quyết định."""
    if num_images < 2 or len(records) < num_images:
        raise ValueError("Cần ít nhất 2 ảnh và đủ mẫu đã scan")
    groups = {True: [r for r in records if r["correct"]], False: [r for r in records if not r["correct"]]}
    half = num_images // 2
    if any(len(group) < half for group in groups.values()):
        raise ValueError("Không đủ correct/incorrect; tăng --scan-limit, không dùng checkpoint khác dựa trên test")
    targets = {True: half, False: half}
    if num_images % 2:
        targets[len(groups[True]) > half] += 1
    result, seen = [], set()
    while len(result) < num_images:
        for correct in (True, False):
            if not targets[correct]:
                continue
            bucket = groups[correct]
            choice = next((r for r in bucket if r["label"] not in seen), bucket[0])
            bucket.remove(choice)
            result.append(choice)
            seen.add(choice["label"])
            targets[correct] -= 1
    if len(seen) < 2:
        raise ValueError("Cần ảnh từ nhiều lớp để trực quan hóa")
    return result


def _plot_panels(axes, result: dict, record: dict, names: list[str]) -> None:
    views = [result["image"], overlay_heatmap(result["image"], result["cls_map"]),
             overlay_heatmap(result["image"], result["rollout_map"])]
    label = f"#{record['index']} {'correct' if record['correct'] else 'incorrect'}"
    title = f"{label}\nTrue: {names[record['label']]}\nPred: {names[record['prediction']]} (p={record['confidence']:.3f})"
    for ax, view, caption in zip(axes, views, [title, "CLS attention (last layer)", "Attention rollout"]):
        ax.imshow(view)
        ax.set_title(caption, fontsize=8)
        ax.axis("off")


def generate_visualizations(
    checkpoint_path: str | Path, *, cache_dir: str | Path | None = None,
    class_names_path: str | Path = "outputs/results/class_names.json", split: str = "val",
    num_images: int = 12, scan_limit: int = 512, seed: int = 42, device: str = "cpu",
    output_dir: str | Path | None = None, expected_sha256: str | None = None,
) -> dict:
    """Scan một tập con cố định để chọn hình; không đo accuracy hoặc chọn mô hình trên test."""
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    if split not in ("val", "test") or num_images < 2 or scan_limit < num_images:
        raise ValueError("split phải val/test; num_images >= 2 và scan_limit >= num_images")
    model, metadata = load_vit_checkpoint(checkpoint_path, device, expected_sha256)
    cfg, names = deepcopy(metadata["config"]), metadata["class_names"]
    prepared_names = json.loads(Path(class_names_path).read_text(encoding="utf-8"))
    if prepared_names != names:
        raise ValueError("class_names của cache không cùng thứ tự checkpoint")
    if cache_dir is not None:
        cfg["data"]["cache_dir"] = str(cache_dir)
    cfg["data"]["num_workers"] = 0
    dataset = build_loader(cfg, split).dataset
    raw = np.load(dataset.x_path, mmap_mode="r")
    size = cfg["data"]["img_size"]
    if (raw.dtype != np.uint8 or raw.shape != (len(dataset), size, size, 3)
            or dataset.y.dtype != np.int64 or (dataset.y < 0).any() or (dataset.y >= len(names)).any()):
        raise ValueError("cache ảnh/nhãn không đúng định dạng hoặc không khớp checkpoint")
    order = np.random.default_rng(seed).permutation(len(dataset))[:scan_limit]
    records = []
    batch_size = cfg["data"]["batch_size"]
    with torch.inference_mode():
        for start in range(0, len(order), batch_size):
            indices = order[start:start + batch_size]
            batch = torch.stack([dataset[int(i)][0] for i in indices]).to(device)
            probabilities = model(batch).float().softmax(dim=-1).cpu()
            confidence, predictions = probabilities.max(dim=-1)
            for index, pred, prob in zip(indices, predictions.tolist(), confidence.tolist()):
                label = int(dataset.y[index])
                records.append({"index": int(index), "label": label, "prediction": pred,
                                "confidence": prob, "correct": pred == label})
    selected = select_examples(records, num_images)
    run_name = make_run_name(cfg)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", run_name):
        raise ValueError("run_name trong checkpoint không hợp lệ cho tên thư mục")
    out = Path(output_dir) if output_dir is not None else Path("outputs/figures/attention") / f"{run_name}_{split}"
    out.mkdir(parents=True, exist_ok=True)
    gallery = Figure(figsize=(9, 2.7 * num_images))
    FigureCanvasAgg(gallery)
    grid_axes = gallery.subplots(num_images, 3, squeeze=False)
    cls_maps, rollout_maps, examples = [], [], []
    for row, record in enumerate(selected):
        result = explain_image(model, Image.fromarray(np.array(raw[record["index"]])), cfg)
        probability = result["logits"].softmax(dim=-1)
        if int(probability.argmax()) != record["prediction"]:
            raise ValueError("Dự đoán hai nhánh khác nhau; cần kiểm tra trước khi xuất hình")
        record = {**record, "confidence": float(probability.max()),
                  "label_name": names[record["label"]], "prediction_name": names[record["prediction"]]}
        filename = f"{row + 1:02d}_{record['index']:05d}_{'correct' if record['correct'] else 'incorrect'}.png"
        figure = Figure(figsize=(9, 3))
        FigureCanvasAgg(figure)
        _plot_panels(figure.subplots(1, 3), result, record, names)
        figure.tight_layout()
        figure.savefig(out / filename, dpi=120)
        _plot_panels(grid_axes[row], result, record, names)
        cls_maps.append(result["cls_map"].numpy())
        rollout_maps.append(result["rollout_map"].numpy())
        examples.append({**record, "figure": filename})
    gallery.tight_layout()
    gallery.savefig(out / "gallery.png", dpi=120)
    np.savez_compressed(out / "maps.npz", cls=np.stack(cls_maps), rollout=np.stack(rollout_maps))
    manifest = {"task": "TASK-008", "checkpoint": metadata, "split": split,
                "cache_dir": Path(cfg["data"]["cache_dir"]).as_posix(),
                "selection_seed": seed, "scanned_images": len(order), "scan_limit": scan_limit,
                "selection": "balanced correct/incorrect, prefer distinct true classes; not an accuracy sample",
                "num_images": num_images, "unique_classes": len({e["label"] for e in examples}),
                "test_accuracy": None, "gallery": "gallery.png", "maps": "maps.npz", "examples": examples}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    # PowerShell có thể dùng cp1258, không in được đầy đủ mô tả/lỗi tiếng Việt.
    # Chỉ chỉnh stream của CLI, không chỉnh khi module được import trong demo.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--cache-dir")
    parser.add_argument("--class-names", default="outputs/results/class_names.json")
    parser.add_argument("--split", choices=("val", "test"), default="val")
    parser.add_argument("--num-images", type=int, default=12)
    parser.add_argument("--scan-limit", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--output-dir")
    parser.add_argument("--expected-sha256")
    args = parser.parse_args()
    try:
        result = generate_visualizations(args.checkpoint, cache_dir=args.cache_dir,
                                         class_names_path=args.class_names, split=args.split,
                                         num_images=args.num_images, scan_limit=args.scan_limit,
                                         seed=args.seed, device=args.device, output_dir=args.output_dir,
                                         expected_sha256=args.expected_sha256)
    except (ValueError, OSError, RuntimeError, KeyError) as error:
        parser.error(str(error))
    print(json.dumps({"num_images": result["num_images"], "unique_classes": result["unique_classes"],
                      "split": result["split"], "checkpoint_sha256": result["checkpoint"]["sha256"]}))


if __name__ == "__main__":
    main()
