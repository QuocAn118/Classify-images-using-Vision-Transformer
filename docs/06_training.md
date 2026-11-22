# Huấn luyện

**Người giữ:** TV4 (Hđang). **Đầu việc:** TASK-006, TASK-011. **Code:** `src/train.py`.

TASK-006 và TASK-011 hoàn thành. TV1 review và gộp vào `main` ngày 2026-11-20 (không qua PR): 72 test pass, SHA-256 bốn checkpoint khớp, chạy lại val từ checkpoint best khớp log (ViT 47,61 / CNN 58,74 trên CPU fp32). mô tả đầu việc từng lưu tạm trong `docs/tasks/` do chưa có quyền truy cập GitHub, TV1 xóa ngày 2026-11-20 sau khi gộp. TASK-011 đã train đủ 50 epoch cho hai mô hình, có bằng chứng bên dưới.

## Thành phần làm gì
Train ViT và CNN từ một lệnh, chọn checkpoint trên validation, chịu được ngắt phiên, và ghi log cùng checkpoint theo hợp đồng chung.

## Cấu hình huấn luyện
- AdamW cho cả hai mô hình trong so sánh chính (DEC-002).
- Batch 64, lr 2,5e-4 cho cả ViT và CNN, cùng batch (DEC-003). CNN chỉ đổi lr nếu chỉnh trên validation.
- Warmup 5 epoch rồi cosine về 1e-5, cập nhật theo từng iteration, cosine tính trên tổng 50 epoch.
- 50 epoch, đây là mức sàn (DEC-008).
- Weight decay 0,05, label smoothing 0,1, gradient clipping 1,0.
- Mixup/CutMix với xác suất 0,5 mỗi batch, bật/tắt và xác suất trong config.
- `nn.CrossEntropyLoss` nhận cả nhãn mềm.
- AMP khi có GPU.
- Chọn checkpoint tốt nhất theo validation Top-1, không đọc test.
- Train accuracy không dùng để nhận xét khi bật Mixup/CutMix.

Augmentation trên ảnh nằm ở [04_data.md](04_data.md).

## Hợp đồng

**Tên lần chạy:** `<run_name>` trong các đường dẫn là `<run_name trong YAML>_seed<seed>`, do `train.py` tự sinh để các seed không ghi đè nhau.

**Checkpoint** (`.pt`): `model`, `optimizer`, `scheduler`, `scaler` (trạng thái `GradScaler`, `None` khi không dùng AMP), `epoch`, `best_val_top1`, `config`, `seed`, `class_names`. Demo lấy tên lớp từ `class_names` và mean/std từ `config`. Checkpoint chỉ chứa tensor, dict, list, số và chuỗi; không lưu đối tượng Python hay trạng thái RNG của numpy, để `weights_only=True` nạp được; trạng thái RNG nếu cần lưu thành tensor.

Các khóa bắt buộc trên giữ nguyên. Trainer bổ sung `history` (các dòng CSV), `rng_state` (Python, numpy được chuyển thành số/list, torch/CUDA) và `best_checkpoint` trong file last. Bản best giữ trạng thái model/optimizer/scheduler của đúng epoch đạt val Top-1 cao nhất. Snapshot này giúp khôi phục cả best và CSV khi file bị thiếu, bị ngắt giữa các lần ghi, hoặc resume từ last cũ hơn log; file last lớn hơn vì chứa cả trạng thái best. Các bên đánh giá/demo tiếp tục dùng các khóa bắt buộc như trước.

File: `outputs/checkpoints/<run_name>_last.pt`, `<run_name>_best.pt`. Epoch đánh số từ 1. CSV/checkpoint/ảnh được ghi qua file tạm cùng thư mục rồi đổi tên; lỗi ghi giữ bản cũ. Không resume thì một lần chạy có sẵn sẽ bị từ chối để tránh mất kết quả.

**Log CSV** (`outputs/logs/<run_name>.csv`): `epoch, train_loss, train_acc, val_loss, val_top1, val_top5, lr, epoch_time_s`.

Bên dùng: [07_evaluation.md](07_evaluation.md), [08_demo.md](08_demo.md). Muốn đổi thì sửa ở đây và báo cả nhóm.

## Luồng cài đặt và resume

1. Nạp/kiểm tra config, đặt seed; tạo model qua `build_model(cfg)` và loader chỉ cho `train`, `val`.
2. AdamW chia hai nhóm: weight decay cho trọng số, không áp dụng cho bias, normalization, CLS token và positional embedding. Lịch warmup/cosine bước theo cập nhật optimizer; AMP bỏ bước vì overflow thì scheduler cũng không tiến.
3. Mixup/CutMix chọn ngẫu nhiên một phép trong các phép có alpha dương, áp với xác suất `mix_prob`. CutMix chỉnh hệ số nhãn theo diện tích hộp thật sau khi cắt ở biên. Loss là CrossEntropy với label smoothing cho cả nhãn cứng và mềm.
4. Validation không có Mixup/CutMix, Top-1/Top-5 tính bằng phần trăm, loss trung bình theo số ảnh. `train_acc` vẫn ghi so với nhãn gốc để giữ CSV, không dùng nhận xét chất lượng khi có nhãn trộn.
5. Chọn best bằng validation Top-1; checkpoint last kèm lịch sử và trạng thái RNG. `--resume` khôi phục các trạng thái rồi chạy từ epoch kế tiếp, dựng lại CSV từ checkpoint để không trùng dòng.

Resume phải giữ model, seed, số epoch tổng, công thức train, batch/augmentation và thứ tự tên lớp. Cho phép đổi đường dẫn dữ liệu và số worker khi chuyển máy. Độ dài loader phải giữ nguyên để không lệch lịch learning rate. `--epochs` là tổng số epoch của lịch, không phải số epoch cộng thêm khi resume. Số worker khác nhau/GPU có thể làm kết quả khác vì augmentation và kernel; không hứa trọng số bit-identical trên GPU.

`--quick` giữ kiến trúc, kích thước ảnh và batch trong YAML (để đo bộ nhớ), chạy tối đa 2 epoch × 2 batch train/val. Nó thêm `_quick` vào tên gốc, ví dụ `vit_small_quick_seed42`, nên không ghi đè lần train thật. Không dùng checkpoint quick để resume train thật. Thiếu bất kỳ cache train/val nào thì cả hai loader quick dùng dữ liệu giả với cảnh báo; chế độ train thật luôn báo lỗi nếu thiếu cache. Không đọc cache test.

## FR-004: Huấn luyện
- **Người sử dụng:** TV4.
- **Mục đích:** Train được từ một lệnh và chịu được ngắt phiên.
- **Đầu vào:** Config, dữ liệu đã chuẩn bị.
- **Luồng bình thường:** Mỗi epoch train, đánh giá validation, ghi log, lưu checkpoint tốt nhất và cuối.
- **Quy tắc:** Chọn checkpoint theo validation Top-1, không đọc test; AdamW cho kết quả so sánh chính; lr của CNN mặc định 2,5e-4, nếu chỉnh thì chỉ dựa trên validation; tên lần chạy gồm cả seed.
- **Lỗi và biên:** `--resume` tiếp tục không trùng dòng log; phiên bị ngắt lúc lưu không hỏng checkpoint cũ; không có GPU thì dùng CPU.
- **Kết quả:** Checkpoint, log CSV, hình đường cong học.

## Tiêu chí nghiệm thu

| Mã | Điều kiện ban đầu | Thao tác | Kết quả mong đợi |
|---|---|---|---|
| AC-007 | Không có dữ liệu thật, CPU | Chạy train với `--quick` | Dùng dữ liệu giả và in cảnh báo; kết thúc không lỗi, có checkpoint và log CSV |
| AC-008 | Train bị ngắt sau epoch k | Chạy `--resume` | Tiếp tục từ epoch k+1, log không trùng dòng, lr schedule khớp với chạy liền mạch (chênh không quá 1e-8), `val_loss` ở epoch k+1 chênh không quá 10% so với epoch k (không đòi trọng số giống hệt, vì shuffle, augmentation và GPU không tất định) |

Ở các epoch đầu `val_loss` có thể giảm hơn 10% một cách bình thường, nên khi kiểm tra AC-008 nên ngắt sau giai đoạn warmup (sau epoch 5).

## Xử lý lỗi

| Tình huống | Cách xử lý |
|---|---|
| Chưa có mảng cache | `--quick` dùng dữ liệu giả và in cảnh báo; train thật báo lỗi |
| Train bị ngắt (máy GPU tắt, mất điện, phiên Kaggle/Colab hết giờ) | Ghi file tạm rồi đổi tên (DEC-005), chạy lại bằng `--resume` |
| Resume từ checkpoint cũ hơn log | Các dòng log từ epoch đó trở đi được ghi đè |
| Checkpoint từ người khác | Nạp với `weights_only=True` |

## Kiểm tra cần làm khi có code

| Kiểm tra | Mong đợi |
|---|---|
| Train bị ngắt rồi resume | Như AC-008 |
| Phiên bị ngắt lúc đang lưu checkpoint | Checkpoint cũ không hỏng |
| Nạp checkpoint bằng `weights_only=True` | Nạp được, có đủ `scaler` và `class_names` |
| Chạy hai seed khác nhau | Log, checkpoint và kết quả nằm ở hai tên khác nhau, không ghi đè |
| `--quick` khi chưa có cache; train thật khi chưa có cache | `--quick` dùng dữ liệu giả và cảnh báo; train thật báo lỗi |
| `--quick` trên máy GPU của thành viên | Chạy được, xác nhận đang dùng CUDA |
| VRAM đỉnh | ViT và CNN ở batch 64 đều không lỗi hết bộ nhớ trên 6GB; nếu lỗi thì dùng gradient accumulation hoặc giảm batch còn 32 với cả hai mô hình |

## Cách chạy

| Mục đích | Lệnh | Điều kiện | Trạng thái |
|---|---|---|---|
| Smoke test CPU | `python -m src.train --config configs/vit_small.yaml --quick --device cpu` | Không cần dữ liệu thật; đổi config để kiểm tra CNN | Đã kiểm tra, xem bằng chứng dưới |
| Smoke test CUDA | `python -m src.train --config configs/cnn_baseline.yaml --quick --device cuda` | PyTorch CUDA, GPU khả dụng | Đã kiểm tra batch 64 |
| Train ViT | `python -m src.train --config configs/vit_small.yaml` | Cache và class_names đã chuẩn bị | Đã chạy đủ 50 epoch, xem bằng chứng TASK-011 |
| Train CNN | `python -m src.train --config configs/cnn_baseline.yaml` | Như ViT, chạy sau ViT trên cùng GPU | Đã chạy đủ 50 epoch, xem bằng chứng TASK-011 |
| Resume | `python -m src.train --config configs/vit_small.yaml --resume outputs/checkpoints/vit_small_seed42_last.pt` | Giữ nguyên lịch/config, có checkpoint last | Đã kiểm tra ngắt sau warmup bằng cache giả |

Mặc định tự chọn CUDA nếu có, nếu không dùng CPU. `--device cpu`/`cuda` để chọn rõ; yêu cầu CUDA khi không có GPU sẽ báo lỗi. `--seed S` tách tên lần chạy. Cấu hình thật giữ 50 epoch là mức sàn; không dùng số epoch rút gọn của kiểm thử làm kết quả cuối.

Trên Windows trong repo này có thể dùng `.venv/Scripts/python.exe` thay `python`. Nếu terminal/pipe lỗi mã hóa đường dẫn tiếng Việt, đặt `$env:PYTHONUTF8 = "1"` và `$env:PYTHONIOENCODING = "utf-8"` trong PowerShell trước khi chạy.

## Bằng chứng TASK-006

- Kiểm thử hồi quy: `python -m pytest -q -W error --basetemp .git/codex/pytest-task006-final --tb=short` (thư mục tạm riêng vì thư mục pytest mặc định trên máy bị Access denied).
- Chi tiết môi trường, kết quả và smoke test cấu hình mặc định: [task006_training_checks.json](../outputs/results/task006_training_checks.json).
- Test resume dùng mô hình nhỏ và cache giả chỉ có train/val, ngắt sau epoch 6 trong lịch 8 epoch (warmup 5), sửa log thành dữ liệu cũ/sai và mô phỏng best không khớp; so sánh learning rate từng bước với chạy liên tục ở ngưỡng 1e-8, loss và CSV không trùng. Đây là kiểm chứng AC-008 trên CPU, không phải kết quả Tiny ImageNet.
- Chưa mô phỏng mất điện thật; chưa kiểm tra GPU 6GB khác của nhóm. VRAM trong bằng chứng là lượng tensor cấp phát đỉnh trên RTX 5060 Laptop 8GB, không phải cam kết cho mọi GPU.

**Lưu ý vận hành:**
- Chạy `--quick` trên CPU trước khi tốn giờ GPU.
- Nếu máy GPU chạy Windows thì dùng `if __name__ == "__main__":`, kiểm tra `num_workers` trên Windows, không dùng `torch.compile`. Khi `num_workers=0` thì không bật `persistent_workers` (PyTorch báo lỗi).
- Lưu checkpoint thường xuyên và sao lưu ra ngoài máy GPU (Google Drive hoặc Kaggle Dataset), vì cả nhóm phụ thuộc vào một máy.

## Bằng chứng TASK-011

Đã chạy lần lượt ViT rồi CNN trên cùng RTX 5060 Laptop 8GB với seed 42, batch 64, 50 epoch, cùng phần data/train trong YAML. Không chạy ablation hoặc đánh giá test.

| Model | Epoch best / tổng | Val Top-1 (%) | Val Top-5 tại best (%) | Giây/epoch trung bình | VRAM tensor đỉnh (MiB) |
|---|---:|---:|---:|---:|---:|
| ViT-small | 50 / 50 | 47,63 | 71,77 | 31,94 | 498,97 |
| ResNet-small | 50 / 50 | 58,73 | 81,03 | 22,36 | 320,47 |

Nguồn: [task011_training_checks.json](../outputs/results/task011_training_checks.json), [CSV ViT](../outputs/logs/vit_small_seed42.csv), [CSV CNN](../outputs/logs/cnn_baseline_seed42.csv). Đã kiểm tra 50 dòng không trùng, loss hữu hạn, config data/train/seed bằng nhau, nhãn 450 train / 50 val mỗi lớp; best khớp CSV và snapshot trong last. Model từ checkpoint best nạp lại trên CPU bằng `torch.load(..., map_location="cpu", weights_only=True)` qua `build_model`, logits hữu hạn `(2,200)`.

Checkpoint local: `outputs/checkpoints/vit_small_seed42_{best,last}.pt` và `cnn_baseline_seed42_{best,last}.pt`; không commit. File JSON có SHA-256 để đối chiếu khi sao chép. Chưa có link chia sẻ/offsite backup. Thời gian gồm train/validation, không gồm ghi checkpoint/vẽ hình; VRAM là max_memory_allocated chia 1024² (MiB), không phải toàn bộ bộ nhớ driver. Các trường JSON có hậu tố `_mb` giữ tên cũ của hợp đồng, đơn vị được ghi rõ trong bằng chứng.

TASK-006 và TASK-011 đã có bằng chứng triển khai/chạy, chưa đánh dấu Hoàn thành trước khi TV1 review; chưa có Issue/PR/Projects mới vì chưa có quyền GitHub.

## Rủi ro

| Rủi ro | Ảnh hưởng | Cách xử lý |
|---|---|---|
| Chỉ một máy GPU, các lần train phải chạy lần lượt | Không đủ thí nghiệm | Thời gian mỗi epoch là dự đoán (xem bảng giả định trong [01_define.md](01_define.md)); đo thật trước khi chốt số thí nghiệm; cắt việc theo [03_plan.md](03_plan.md); Kaggle hoặc Colab dự phòng |
| 6GB VRAM không đủ | Lỗi hết bộ nhớ | Đo VRAM đỉnh trước; gradient accumulation hoặc batch 32 cho cả hai mô hình |
| Máy GPU hỏng hoặc chủ máy bận | Trễ toàn bộ train | Sao lưu checkpoint ra ngoài máy; chuyển Kaggle hoặc Colab và `--resume` |
| Mixup/CutMix có thể lợi cho ViT hơn CNN | So sánh thiên lệch | Nêu trong báo cáo; ablation nếu còn thời gian |
