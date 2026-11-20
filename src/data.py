"""DataLoader đọc mảng cache của prepare_data.py (TASK-003, FR-001).

    loader = build_loader(cfg, "train")   # "train" | "val" | "test"

train.py chỉ gọi "train" và "val"; evaluate.py dùng "test" lấy số cuối.
attention.py chỉ đọc "test" tường minh để vẽ với checkpoint đã chốt (docs/04_data.md).
Mixup/CutMix áp ở vòng lặp train, không ở đây.
"""
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import v2

SPLITS = ("train", "val", "test")


def build_transform(cfg, train):
    d = cfg["data"]
    to_float = [v2.ToDtype(torch.float32, scale=True), v2.Normalize(d["mean"], d["std"])]
    if not train:
        return v2.Compose(to_float)
    aug = [v2.RandomCrop(d["img_size"], padding=4), v2.RandomHorizontalFlip()]
    if d.get("randaugment"):
        aug.append(v2.RandAugment())  # chạy trên uint8, trước khi đổi sang float
    erasing = [v2.RandomErasing(p=d["random_erasing"])] if d.get("random_erasing", 0) > 0 else []
    return v2.Compose(aug + to_float + erasing)


class CachedDataset(Dataset):
    """Ảnh uint8 NHWC trong file .npy, mở bằng mmap lười để mỗi worker tự mở, không pickle cả mảng."""

    def __init__(self, x_path, y, transform):
        self.x_path, self.y, self.transform = str(x_path), y, transform
        self._x = None

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        if self._x is None:
            self._x = np.load(self.x_path, mmap_mode="r")
        img = torch.from_numpy(np.array(self._x[i])).permute(2, 0, 1)  # copy vì mmap chỉ đọc
        return self.transform(img), int(self.y[i])

    def __getstate__(self):
        return {**self.__dict__, "_x": None}


def build_loader(cfg, split):
    if split not in SPLITS:
        raise ValueError(f"split phải là một trong {SPLITS}, nhận '{split}'")
    d = cfg["data"]
    cache = Path(d["cache_dir"])
    x_path, y_path = cache / f"{split}_x.npy", cache / f"{split}_y.npy"
    if not (x_path.exists() and y_path.exists()):
        raise FileNotFoundError(f"Không thấy cache '{x_path}'. Chạy trước: python scripts/prepare_data.py --download")
    train = split == "train"
    ds = CachedDataset(x_path, np.load(y_path), build_transform(cfg, train))
    workers = d["num_workers"]
    return DataLoader(ds, batch_size=d["batch_size"], shuffle=train, drop_last=train,
                      num_workers=workers, pin_memory=torch.cuda.is_available(), persistent_workers=workers > 0)
