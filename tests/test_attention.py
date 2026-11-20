"""TASK-008: kiểm toán công thức, tích hợp checkpoint/cache và đầu ra CLI."""
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image
import pytest
import torch

from src.attention import (
    attention_rollout, cls_attention_map, explain_image, generate_visualizations,
    load_vit_checkpoint, overlay_heatmap, select_examples,
)
from src.models import build_model
from src.utils import atomic_save, load_config


@pytest.fixture(scope="module", autouse=True)
def cpu_threads():
    previous = torch.get_num_threads()
    torch.set_num_threads(1)
    yield
    torch.set_num_threads(previous)


def test_cls_map_uses_final_layer_and_drops_cls_column():
    first = torch.eye(5)[None, None]
    last = first.repeat(2, 2, 1, 1)
    last[:, 0, 0] = torch.tensor([0.0, 0.1, 0.2, 0.3, 0.4])
    last[:, 1, 0] = torch.tensor([0.0, 0.1, 0.1, 0.2, 0.6])
    result = cls_attention_map([first.repeat(2, 2, 1, 1), last], 2, 1)
    # Mean heads -> [.1,.15,.25,.5], min-max -> [0,.125,.375,1].
    expected = torch.tensor([[0.0, 0.125], [0.375, 1.0]]).expand(2, 2, 2)
    torch.testing.assert_close(result, expected, rtol=0, atol=1e-6)


def test_rollout_residual_and_layer_multiplication_order():
    first = torch.eye(5)[None, None]
    second = first.clone()
    first[0, 0, 0] = torch.tensor([0, 1, 0, 0, 0])
    second[0, 0, 0] = torch.tensor([0, 0, 1, 0, 0])
    # (I+A2)/2 @ (I+A1)/2 gives CLS row [1/4,1/4,1/2,0,0].
    expected = torch.tensor([[[0.5, 1.0], [0.0, 0.0]]])
    torch.testing.assert_close(attention_rollout([first, second], 2, 1), expected)
    assert not torch.allclose(attention_rollout([second, first], 2, 1), expected)


@pytest.mark.parametrize("fn", [cls_attention_map, attention_rollout])
def test_constant_maps_are_finite_zero_without_changing_input(fn):
    weights = torch.eye(5).repeat(2, 3, 1, 1)
    before = weights.clone()
    result = fn([weights], 8, 4)
    assert result.shape == (2, 8, 8) and result.dtype == torch.float32
    assert torch.isfinite(result).all() and torch.count_nonzero(result) == 0
    assert torch.equal(weights, before)


@pytest.mark.parametrize("fn", [cls_attention_map, attention_rollout])
def test_maps_use_head_average_and_resize_to_config(fn):
    weights = torch.eye(17).repeat(2, 3, 1, 1)
    weights[:, :, 0] = torch.arange(17, dtype=torch.float32) / 136
    result = fn([weights], 32, 8)
    assert result.shape == (2, 32, 32)
    assert result.min() == 0 and result.max() == 1
    assert result[0, 0, 0] < result[0, -1, -1]


@pytest.mark.parametrize("weights,size,patch", [
    ([], 8, 4), ([torch.ones(1, 1, 4, 4)], 8, 4),
    ([torch.full((1, 1, 5, 5), float("nan"))], 8, 4),
    ([torch.ones(1, 1, 5, 5)], 7, 4),
])
def test_invalid_attention_or_grid_is_rejected(weights, size, patch):
    with pytest.raises(ValueError):
        attention_rollout(weights, size, patch)


@pytest.mark.parametrize("mode", ["RGB", "L", "RGBA"])
def test_overlay_converts_to_rgb_and_alpha_zero_preserves_image(mode):
    image = Image.new(mode, (8, 8), 100)
    result = overlay_heatmap(image, torch.zeros(8, 8), alpha=0)
    assert result.mode == "RGB" and result.size == (8, 8)
    assert np.array_equal(np.asarray(result), np.asarray(image.convert("RGB")))


def test_overlay_rejects_wrong_shape_or_alpha():
    image = Image.new("RGB", (8, 8))
    with pytest.raises(ValueError):
        overlay_heatmap(image, torch.ones(4, 4))
    with pytest.raises(ValueError):
        overlay_heatmap(image, torch.zeros(8, 8), alpha=1.2)


def test_selection_balances_groups_and_prefers_distinct_classes():
    rows = [{"index": i, "label": label, "correct": correct}
            for i, (label, correct) in enumerate([(0, True), (0, True), (1, False), (2, True), (3, False), (1, False)])]
    selected = select_examples(rows, 4)
    assert sum(r["correct"] for r in selected) == 2
    assert len({r["label"] for r in selected}) == 4
    assert selected == select_examples(rows, 4)


def test_selection_fails_instead_of_claiming_acceptance_for_only_correct_images():
    with pytest.raises(ValueError, match="correct|incorrect"):
        select_examples([{"index": i, "label": i, "correct": True} for i in range(12)], 12)


@pytest.fixture
def checkpoint_case(tmp_path):
    cfg = load_config(Path(__file__).resolve().parents[1] / "configs/vit_small.yaml")
    cfg["run_name"] = "attention_unit_test"
    cfg["data"].update(img_size=16, num_classes=3, batch_size=4, num_workers=0)
    cfg["model"].update(embed_dim=24, depth=2, num_heads=3, patch_size=4)
    torch.manual_seed(42)
    model = build_model(cfg).eval()
    # Predictable labels: every input predicts class 0, so cache has both groups.
    with torch.no_grad():
        model.head.weight.zero_()
        model.head.bias.copy_(torch.tensor([2.0, 0.0, 0.0]))
    names = ["zero", "one", "two"]
    path = tmp_path / "unit_test.pt"
    atomic_save({"model": model.state_dict(), "config": cfg, "class_names": names,
                 "epoch": 0, "seed": 42, "best_val_top1": 0.0}, path)
    cache = tmp_path / "cache"
    cache.mkdir()
    rng = np.random.default_rng(42)
    np.save(cache / "val_x.npy", rng.integers(0, 256, (12, 16, 16, 3), dtype=np.uint8))
    np.save(cache / "val_y.npy", np.array([0, 1, 2] * 4, dtype=np.int64))
    names_path = tmp_path / "class_names.json"
    names_path.write_text(json.dumps(names), encoding="utf-8")
    return path, cfg, cache, names_path


def test_checkpoint_loading_and_single_image_explanation(checkpoint_case):
    path, cfg, _, _ = checkpoint_case
    model, metadata = load_vit_checkpoint(path)
    assert not model.training and metadata["epoch"] == 0
    assert metadata["config"] == cfg and len(metadata["sha256"]) == 64
    result = explain_image(model, Image.new("RGBA", (25, 17), (100, 80, 30, 100)), cfg)
    assert result["image"].mode == "RGB" and result["image"].size == (16, 16)
    assert result["logits"].shape == (3,)
    assert result["cls_map"].shape == result["rollout_map"].shape == (16, 16)
    assert result["logits"].argmax().item() == 0


def test_checkpoint_hash_and_class_names_are_validated(checkpoint_case, tmp_path):
    path, _, _, _ = checkpoint_case
    with pytest.raises(ValueError, match="SHA"):
        load_vit_checkpoint(path, expected_sha256="0" * 64)
    checkpoint = torch.load(path, weights_only=True)
    checkpoint["class_names"] = ["missing"]
    atomic_save(checkpoint, tmp_path / "invalid.pt")
    with pytest.raises(ValueError, match="class_names"):
        load_vit_checkpoint(tmp_path / "invalid.pt")


def test_end_to_end_gallery_records_provenance_and_never_reads_test(checkpoint_case, tmp_path):
    path, _, cache, names = checkpoint_case
    out = tmp_path / "attention"
    manifest = generate_visualizations(path, cache_dir=cache, class_names_path=names,
                                       num_images=4, scan_limit=12, output_dir=out)
    assert manifest["split"] == "val" and manifest["scanned_images"] == 12
    assert len(manifest["examples"]) == 4
    assert sum(e["correct"] for e in manifest["examples"]) == 2
    assert manifest["checkpoint"]["epoch"] == 0
    assert manifest["test_accuracy"] is None
    for item in manifest["examples"]:
        assert (out / item["figure"]).exists()
    assert (out / "gallery.png").exists() and (out / "maps.npz").exists()
    assert json.loads((out / "manifest.json").read_text(encoding="utf-8")) == manifest
    assert not (cache / "test_x.npy").exists()


def test_wrong_label_order_is_rejected_before_visualization(checkpoint_case, tmp_path):
    path, _, cache, names = checkpoint_case
    names.write_text(json.dumps(["one", "zero", "two"]), encoding="utf-8")
    with pytest.raises(ValueError, match="class_names"):
        generate_visualizations(path, cache_dir=cache, class_names_path=names,
                                num_images=4, output_dir=tmp_path / "wrong")


def test_cli_help_works_with_windows_legacy_output_encoding():
    env = {**os.environ, "PYTHONIOENCODING": "cp1258"}
    result = subprocess.run([sys.executable, "-m", "src.attention", "--help"],
                            cwd=Path(__file__).resolve().parents[1], env=env,
                            capture_output=True, encoding="utf-8", timeout=60)
    assert result.returncode == 0, result.stderr
    assert "--checkpoint" in result.stdout
