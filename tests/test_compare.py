import csv
import json
import pytest
from src import compare


@pytest.mark.parametrize("top1", [50., None])
def test_comparison_without_optional_measurements(tmp_path, monkeypatch, top1):
    monkeypatch.chdir(tmp_path)
    results = tmp_path / "outputs/results"
    results.mkdir(parents=True)
    for name, model in [("vit_small_seed42", "vit"), ("cnn_baseline_seed42", "resnet_small")]:
        (results / (name + ".json")).write_text(json.dumps(dict(model=model, seed=42, params=10, top1=top1, top5=80.)))
    compare.main()
    with (results / "comparison.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[0]["flops_per_image"] == rows[0]["macs"] == "chưa có"
    assert rows[0]["top1"] == ("chưa có" if top1 is None else "50.0")
    assert "chưa có" in (results / "comparison.md").read_text(encoding="utf-8")
    assert (tmp_path / "outputs/figures/comparison_test_top1.png").is_file()
