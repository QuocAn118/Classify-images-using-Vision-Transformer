import csv
import numpy as np
import pytest
from scripts import error_analysis


@pytest.mark.parametrize("wrong_count", [0, 1, 3])
def test_error_grid_accepts_fewer_than_twenty_errors(tmp_path, monkeypatch, wrong_count):
    monkeypatch.chdir(tmp_path)
    with (tmp_path / "unit_predictions.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image_index", "true_label", "pred_label", "confidence"])
        for i in range(wrong_count):
            writer.writerow([i, 0, 1, .9])
    error_analysis.save_error_grid("unit", tmp_path, ["a", "b"], np.zeros((3, 8, 8, 3), dtype=np.uint8))
    assert (tmp_path / "outputs/figures/errors_unit.png").is_file()


def test_class_ranking_skips_unobserved_classes(tmp_path):
    (tmp_path / "unit_per_class.csv").write_text("class_id,class_name,correct,total,accuracy_pct\n0,absent,0,0,\n1,seen,1,1,100\n")
    error_analysis.save_class_ranking("unit", tmp_path)
    text = (tmp_path / "unit_class_ranking.csv").read_text()
    assert "seen" in text and "absent" not in text


def test_error_grid_keeps_labels_visible(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "unit_predictions.csv").write_text("image_index,true_label,pred_label,confidence\n0,0,1,0.9\n")
    captured = []
    original_close = error_analysis.plt.close
    monkeypatch.setattr(error_analysis.plt, "close", lambda fig: captured.append(fig))
    error_analysis.save_error_grid("unit", tmp_path, ["cat", "dog"], np.zeros((1, 8, 8, 3), dtype=np.uint8))
    fig = captured[-1]
    assert fig.axes[0].axison
    assert "True: cat" in fig.axes[0].get_xlabel()
    assert not fig.axes[1].axison
    original_close(fig)
