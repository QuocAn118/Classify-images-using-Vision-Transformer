"""TASK-006: dữ liệu giả nhỏ, không có cache test, không đo accuracy thật."""
from copy import deepcopy
import csv
import json
from pathlib import Path

import numpy as np
import pytest
import torch

import src.train as training
from src.models import build_model
from src.utils import load_config

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module", autouse=True)
def cpu_threads():
    previous = torch.get_num_threads()
    torch.set_num_threads(1)
    yield
    torch.set_num_threads(previous)


@pytest.fixture
def cfg(tmp_path):
    cfg = load_config(ROOT / "configs/vit_small.yaml")
    cfg["data"].update(cache_dir=str(tmp_path / "cache"), img_size=16, batch_size=4,
                       num_workers=0, num_classes=7, randaugment=False)
    cfg["model"].update(patch_size=4, embed_dim=16, depth=1, num_heads=2, drop_path_rate=0)
    cfg["train"].update(epochs=8, mix_prob=0.0)
    return cfg


def prepare_cache(cfg, out):
    cache = Path(cfg["data"]["cache_dir"])
    cache.mkdir(exist_ok=True)
    rng = np.random.default_rng(42)
    for split, n in (("train", 12), ("val", 9)):
        np.save(cache / f"{split}_x.npy", rng.integers(256, size=(n, 16, 16, 3), dtype=np.uint8))
        np.save(cache / f"{split}_y.npy", np.arange(n, dtype=np.int64) % 7)
    (out / "results").mkdir(parents=True)
    (out / "results/class_names.json").write_text(json.dumps([f"class_{i}" for i in range(7)]))


@pytest.mark.parametrize("model", ["vit", "resnet_small"])
def test_cpu_quick_without_cache_updates_model_and_saves_contract(cfg, tmp_path, capsys, model):
    if model == "resnet_small":
        cfg["model"] = {"name": model, "widths": [4, 8, 16, 32], "blocks": [1, 1, 1, 1], "stem_stride": 2}
    original = deepcopy(cfg)
    training.set_seed(cfg["seed"])
    initial = {key: value.clone() for key, value in build_model(cfg).state_dict().items()}
    result = training.train(cfg, quick=True, device="cpu", out_dir=tmp_path / "outputs")
    assert "CẢNH BÁO" in capsys.readouterr().out
    assert cfg == original
    assert result["synthetic"] and result["run_name"] == "vit_small_quick_seed42"
    checkpoint = torch.load(result["last_checkpoint"], weights_only=True)
    assert {"model", "optimizer", "scheduler", "scaler", "epoch", "best_val_top1", "config", "seed", "class_names"} <= checkpoint.keys()
    assert checkpoint["scaler"] is None and checkpoint["epoch"] == 2
    assert len(checkpoint["class_names"]) == 7
    assert any(not torch.equal(value, initial[key]) for key, value in checkpoint["model"].items())
    best = torch.load(result["best_checkpoint"], weights_only=True)
    assert best["best_val_top1"] == max(row["val_top1"] for row in result["history"])
    assert (tmp_path / "outputs/figures/vit_small_quick_seed42_curves.png").is_file()
    with pytest.raises(FileExistsError, match="resume"):
        training.train(cfg, quick=True, device="cpu", out_dir=tmp_path / "outputs")


def test_real_train_requires_cache_and_never_falls_back(cfg, tmp_path):
    with pytest.raises(FileNotFoundError, match="prepare_data"):
        training.train(cfg, device="cpu", out_dir=tmp_path / "outputs")
    assert not (tmp_path / "outputs/checkpoints").exists()


def test_two_seeds_do_not_overwrite_outputs(cfg, tmp_path):
    first = training.train(cfg, quick=True, device="cpu", out_dir=tmp_path / "outputs")
    cfg["seed"] = 43
    second = training.train(cfg, quick=True, device="cpu", out_dir=tmp_path / "outputs")
    assert first["last_checkpoint"] != second["last_checkpoint"]
    assert Path(first["last_checkpoint"]).exists() and Path(second["last_checkpoint"]).exists()


def test_resume_after_warmup_matches_uninterrupted_and_repairs_stale_log(cfg, tmp_path, monkeypatch):
    cfg["train"]["mix_prob"] = 1.0
    full, interrupted = tmp_path / "full", tmp_path / "interrupted"
    prepare_cache(cfg, full)
    prepare_cache(cfg, interrupted)
    traces = []
    original_step = torch.optim.lr_scheduler.LambdaLR.step

    def record_step(scheduler, epoch=None):
        original_step(scheduler, epoch)
        if scheduler.last_epoch > 0:
            traces.append(scheduler.get_last_lr()[0])

    monkeypatch.setattr(torch.optim.lr_scheduler.LambdaLR, "step", record_step)
    complete = training.train(cfg, device="cpu", out_dir=full)
    full_trace, traces[:] = traces[:], []
    original_save = training.atomic_save

    def interrupt_after_checkpoint(obj, path):
        original_save(obj, path)
        if Path(path).name.endswith("_last.pt") and obj["epoch"] == 6:
            raise KeyboardInterrupt("Mô phỏng ngắt phiên sau warmup")

    monkeypatch.setattr(training, "atomic_save", interrupt_after_checkpoint)
    with pytest.raises(KeyboardInterrupt):
        training.train(cfg, device="cpu", out_dir=interrupted)
    monkeypatch.setattr(training, "atomic_save", original_save)
    checkpoint_path = interrupted / "checkpoints/vit_small_seed42_last.pt"
    checkpoint = torch.load(checkpoint_path, weights_only=True)
    assert checkpoint["epoch"] == 6
    log_path = interrupted / "logs/vit_small_seed42.csv"
    with log_path.open("a", newline="") as stream:
        stream.write("8,999,0,999,0,0,999,0\n")
    torch.save({"future_checkpoint": True}, interrupted / "checkpoints/vit_small_seed42_best.pt")
    traces.clear()
    resumed = training.train(cfg, resume=checkpoint_path, device="cpu", out_dir=interrupted)
    assert traces == pytest.approx(full_trace[6 * 3:], abs=1e-8)
    assert [row["epoch"] for row in resumed["history"]] == list(range(1, 9))
    for a, b in zip(complete["history"], resumed["history"]):
        for key in ("train_loss", "val_loss", "val_top1", "val_top5", "lr"):
            assert a[key] == pytest.approx(b[key], abs=1e-8)
    assert abs(resumed["history"][6]["val_loss"] / resumed["history"][5]["val_loss"] - 1) <= 0.1
    with log_path.open(newline="") as stream:
        assert [int(row["epoch"]) for row in csv.DictReader(stream)] == list(range(1, 9))
    best = torch.load(resumed["best_checkpoint"], weights_only=True)
    assert best["best_val_top1"] == max(row["val_top1"] for row in resumed["history"])
    # Train/validation là hai cache duy nhất: đọc nhầm test sẽ gây lỗi.
    assert not (Path(cfg["data"]["cache_dir"]) / "test_x.npy").exists()


@pytest.mark.parametrize("change", ["lr", "batch_size", "quick"])
def test_resume_rejects_incompatible_schedule_or_quick_mode(cfg, tmp_path, change):
    out = tmp_path / "outputs"
    prepare_cache(cfg, out)
    result = training.train(cfg, quick=True, device="cpu", out_dir=out)
    if change == "lr":
        cfg["train"]["lr"] *= 2
    elif change == "batch_size":
        cfg["data"]["batch_size"] *= 2
    with pytest.raises(ValueError, match="Resume"):
        training.train(cfg, quick=change != "quick", resume=result["last_checkpoint"], device="cpu", out_dir=out)


def test_scheduler_warms_up_and_finishes_at_min_lr(cfg):
    model = build_model(cfg)
    opt = training.build_optimizer(model, cfg)
    scheduler = training.build_scheduler(opt, cfg, 3)
    rates = []
    for _ in range(24):
        rates.append(opt.param_groups[0]["lr"])
        opt.step()
        scheduler.step()
    assert rates[0] == pytest.approx(cfg["train"]["lr"] / 15)
    assert max(rates) == pytest.approx(cfg["train"]["lr"])
    assert rates[-1] == pytest.approx(cfg["train"]["min_lr"])
    assert all(a >= b for a, b in zip(rates[15:], rates[16:]))


def test_weight_decay_excludes_bias_norm_and_tokens(cfg):
    model = build_model(cfg)
    optimizer = training.build_optimizer(model, cfg)
    decay_ids = {id(p) for group in optimizer.param_groups if group["weight_decay"] for p in group["params"]}
    params = dict(model.named_parameters())
    assert id(params["patch_embed.proj.weight"]) in decay_ids
    assert not any(id(value) in decay_ids for key, value in params.items()
                   if value.ndim <= 1 or key in ("cls_token", "pos_embed"))


@pytest.mark.parametrize("mode", ["mixup", "cutmix"])
def test_mixed_targets_match_pixel_contribution(cfg, monkeypatch, mode):
    cfg["data"]["num_classes"] = 2
    cfg["train"].update(mix_prob=1.0, mixup_alpha=float(mode == "mixup"), cutmix_alpha=float(mode == "cutmix"))
    monkeypatch.setattr(np.random, "beta", lambda *args: 0.5)
    monkeypatch.setattr(torch, "randperm", lambda n, **kwargs: torch.arange(n - 1, -1, -1, **kwargs))
    x = torch.stack((torch.zeros(3, 16, 16), torch.ones(3, 16, 16)))
    y = torch.tensor([0, 1])
    mixed, targets = training.mix_batch(x, y, cfg)
    assert targets.shape == (2, 2)
    torch.testing.assert_close(targets.sum(1), torch.ones(2))
    torch.testing.assert_close(mixed.mean((1, 2, 3)), targets[:, 1])
    assert torch.nn.CrossEntropyLoss(label_smoothing=0.1)(torch.zeros(len(x), 2), targets).isfinite()


@pytest.mark.parametrize("key,value", [("mix_prob", 1.1), ("mixup_alpha", -1), ("epochs", 0),
                                        ("lr", float("nan")), ("label_smoothing", 1)])
def test_invalid_training_config_is_rejected_before_writing(cfg, tmp_path, key, value):
    cfg["train"][key] = value
    with pytest.raises(ValueError):
        training.train(cfg, quick=True, device="cpu", out_dir=tmp_path / "outputs")
    assert not (tmp_path / "outputs").exists()


def test_failed_csv_write_keeps_old_file_and_cleans_temp(tmp_path, monkeypatch):
    path = tmp_path / "log.csv"
    training.save_log([], path)
    old = path.read_bytes()

    def fail_replace(*args):
        raise OSError("Mô phỏng lỗi đĩa")
    monkeypatch.setattr(training.os, "replace", fail_replace)
    with pytest.raises(OSError):
        training.save_log([], path)
    assert path.read_bytes() == old
    assert list(tmp_path.iterdir()) == [path]


def test_optional_train_settings_have_defaults(cfg, tmp_path):
    cfg["train"] = {key: cfg["train"][key] for key in ("epochs", "optimizer", "lr", "weight_decay")}
    result = training.train(cfg, quick=True, device="cpu", out_dir=tmp_path / "outputs")
    checkpoint = torch.load(result["last_checkpoint"], weights_only=True)
    assert checkpoint["config"]["train"]["mix_prob"] == 0.5
    assert checkpoint["epoch"] == 2
    assert "mix_prob" not in cfg["train"]


def test_resume_best_into_new_output_directory_restores_last_and_best(cfg, tmp_path):
    original = training.train(cfg, quick=True, device="cpu", out_dir=tmp_path / "first")
    resumed = training.train(cfg, quick=True, resume=original["best_checkpoint"], device="cpu", out_dir=tmp_path / "moved")
    last = torch.load(resumed["last_checkpoint"], weights_only=True)
    best = torch.load(resumed["best_checkpoint"], weights_only=True)
    assert last["epoch"] == 2
    assert best["best_val_top1"] == max(row["val_top1"] for row in last["history"])
    assert last["best_checkpoint"] is not None
