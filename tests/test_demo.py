import pytest
import torch
from PIL import Image
from app import demo


@pytest.mark.parametrize("mode", ["RGB", "L", "RGBA"])
def test_predict_uses_config_size_normalization_and_names(mode):
    class Model(torch.nn.Module):
        def forward(self, batch):
            assert batch.shape == (1, 3, 16, 16)
            torch.testing.assert_close(batch, torch.full_like(batch, -1))
            return torch.tensor([[0., 2., 1.]])
    cfg = {"data": {"img_size": 16, "mean": [.5]*3, "std": [.5]*3}}
    result = demo.predict_top5(Model(), Image.new(mode, (30, 20)), cfg, ["a", "b", "c"])
    assert list(result) == ["b", "c", "a"]
    assert sum(result.values()) == pytest.approx(1)


def test_missing_checkpoint_is_readable_without_traceback(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(demo, "CHECKPOINT_DIR", tmp_path)
    assert demo.main() == 1
    error = capsys.readouterr().err
    assert "Thiếu checkpoint" in error and str(tmp_path) in error
    assert "Traceback" not in error


def test_corrupt_checkpoint_is_readable(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(demo, "CHECKPOINT_DIR", tmp_path)
    (tmp_path / "vit_small_seed42_best.pt").write_bytes(b"broken")
    assert demo.main() == 1
    assert "Checkpoint không hợp lệ" in capsys.readouterr().err
