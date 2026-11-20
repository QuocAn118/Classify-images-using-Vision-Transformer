# TASK-011: Train thật ViT và CNN

- **Trạng thái:** Hoàn thành. TV1 review và gộp vào `main` ngày 2026-11-20 (không qua PR): 72 test pass, SHA-256 bốn checkpoint khớp, chạy lại val từ checkpoint best khớp log (ViT 47,61 / CNN 58,74 trên CPU fp32). chưa có Issue GitHub. Tiếp tục lưu mô tả trong repo theo lựa chọn của người dùng ngày 2026-11-19.
- **Người phụ trách / người duyệt:** TV4 (Hđang), nhánh `hoangdang` / TV1.
- **Mục tiêu:** train hai cấu hình chính 50 epoch với seed 42 trên cùng dữ liệu/augmentation, chọn best bằng validation; lưu checkpoint, log, đường cong và phần báo cáo mục 4.
- **Phụ thuộc:** TASK-006 đã kiểm chứng 72 test và quick CPU/CUDA; TV1 đã review và gộp. Máy hiện có RTX 5060 Laptop 8GB, driver 582.05 và PyTorch 2.11.0+cu128; khác giả định GPU 6GB trong kế hoạch.
- **Input:** hai YAML trong configs, cache train/val tạo bằng prepare_data với seed 42, class_names theo cùng thứ tự nhãn. Mỗi máy tự tải dữ liệu theo DEC-015.
- **Output:** checkpoint best/last không commit, CSV, hình đường cong, JSON tóm tắt validation và thời gian/VRAM có nguồn từ log/chạy thật. Số test cuối là phần TV5, ở đây ghi chưa có.
- **Phạm vi:** tải/chuẩn bị cache bằng script sẵn có, kiểm tra nhãn/thống kê, chạy ViT rồi CNN trên cùng GPU, đối chiếu số epoch/best/checkpoint và cập nhật báo cáo TV4. Không giảm mức sàn 50 epoch, không điều chỉnh cấu hình trên test, không làm ablation hoặc phần TV5.
- **Cách kiểm tra:** checkpoint nạp bằng weights_only, epoch cuối 50, CSV đủ 50 epoch không trùng; best_val_top1 bằng max val_top1 trong CSV; loss hữu hạn; cấu hình data/train/seed hai run bằng nhau; model tải lại được. Chưa có file kết quả thật thì không điền accuracy dự đoán.
- **Lệnh:** `python -m src.train --config configs/vit_small.yaml`, sau đó `python -m src.train --config configs/cnn_baseline.yaml`. Nếu ngắt, tiếp tục với --resume đúng file last, giữ nguyên lịch 50 epoch.
- **Giới hạn bàn giao:** không tự commit/push, không chia sẻ checkpoint ra tài khoản ngoài khi chưa có đích lưu; chưa đánh dấu Hoàn thành khi chưa có người duyệt.

## Bằng chứng bàn giao

- Cả ViT và CNN chạy đủ 50 epoch, seed 42, cùng data/train, không đọc test. CSV đủ 50 dòng không trùng; loss/model hữu hạn, checkpoint nạp bằng weights_only, class_names và best khớp lịch sử. Hai model tải lại qua factory trên CPU, logits `(2,200)` hữu hạn.
- ViT: best epoch 50, validation Top-1 47,63%, Top-5 71,77%; 31,94 giây/epoch, 498,97 MiB tensor VRAM đỉnh.
- CNN: best epoch 50, validation Top-1 58,73%, Top-5 81,03%; 22,36 giây/epoch, 320,47 MiB tensor VRAM đỉnh.
- Nguồn: [task011_training_checks.json](../../outputs/results/task011_training_checks.json), CSV/đường cong trong outputs; báo cáo mục 4.2 đã cập nhật. JSON có SHA-256 checkpoint và môi trường/cấu hình.
- Checkpoint local ở outputs/checkpoints, không commit, chưa có link chia sẻ/offsite backup. Chưa có test accuracy, benchmark inference hoặc ablation; các phần này không được thay bằng số validation.
- Chưa commit/push, chưa tạo Issue/PR/Projects trên GitHub hoặc tự đánh dấu Hoàn thành. TV1 cần review bằng chứng.
