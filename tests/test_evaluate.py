import csv
import json
import pytest
import torch
from src import evaluate


def test_metrics_use_all_images_and_keep_prediction_indices():
    logits = torch.tensor([[4., 1., 0.], [3., 2., 1.], [0., 1., 4.]])
    loader = [(logits[:2], torch.tensor([0, 1])), (logits[2:], torch.tensor([2]))]
    metrics, classes, predictions = evaluate.evaluate_model(torch.nn.Identity(), loader, "cpu")
    assert metrics == {"top1": 100*2/3, "top5": 100.}
    assert classes[1]["accuracy_pct"] == 0
    assert [p["image_index"] for p in predictions] == [0, 1, 2]
    assert [p["pred_label"] for p in predictions] == [0, 0, 2]


def test_empty_loader_is_rejected():
    with pytest.raises(ValueError, match="không có ảnh"):
        evaluate.evaluate_model(torch.nn.Identity(), [], "cpu")


def test_save_uses_checkpoint_names_not_external_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    results = tmp_path / "outputs/results"
    results.mkdir(parents=True)
    (results / "class_names.json").write_text('["wrong"]')
    metrics = dict(model="vit", seed=42, params=1, top1=100., top5=100.)
    evaluate.save_results("unit", metrics, {0: dict(correct=1, total=1, accuracy_pct=100)}, [], ["checkpoint", "absent"])
    with (results / "unit_per_class.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert [r["class_name"] for r in rows] == ["checkpoint", "absent"]
    assert rows[1]["accuracy_pct"] == ""
    assert json.loads((results / "unit.json").read_text())["top1"] == 100


def test_speed_rejects_invalid_repeats():
    with pytest.raises(ValueError):
        evaluate.measure_inference_speed(torch.nn.Identity(), torch.ones(1, 3), repeats=0)
