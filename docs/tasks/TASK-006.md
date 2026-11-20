# TASK-006: Vòng lặp train, quick và resume

- **Trạng thái:** Hoàn thành. TV1 review và gộp vào `main` ngày 2026-11-20 (không qua PR): 72 test pass, SHA-256 bốn checkpoint khớp, chạy lại val từ checkpoint best khớp log (ViT 47,61 / CNN 58,74 trên CPU fp32). chưa có Issue/PR GitHub. Người dùng cho phép lưu mô tả trong repo rồi triển khai ngày 2026-11-19 do CLI chưa đăng nhập và không truy cập được GitHub qua Computer Use.
- **Mục tiêu:** train ViT/CNN từ YAML, kiểm tra nhanh trên CPU/CUDA và tiếp tục an toàn từ checkpoint.
- **Người phụ trách / người duyệt:** TV4 (Hđang), nhánh `hoangdang` / TV1.
- **Yêu cầu:** FR-004, AC-007 và AC-008 trong [06_training.md](../06_training.md); TASK-001, 003, 004, 005 đã có trong nhánh.
- **Phạm vi:** `src/train.py`, test train, bằng chứng, hướng dẫn chạy, phần báo cáo TV4 và nhật ký. Dùng `build_loader`, `build_model`, `make_run_name`, `set_seed`, `atomic_save` sẵn có. Không sửa mô hình, không viết phần TV2/TV5, chưa train thật TASK-011 trong khi TASK-006 chưa được kiểm tra.
- **Input:** config YAML; cache train/val; checkpoint tùy chọn. CLI: `--config`, `--quick`, `--epochs`, `--seed`, `--resume`, `--device` (CPU/CUDA để kiểm chứng trên máy có GPU).
- **Output:** checkpoint best/last, CSV theo hợp đồng và đường cong loss/accuracy. Checkpoint giữ đủ các khóa bắt buộc và nạp bằng `weights_only=True`.
- **Hành vi:** AdamW, loại bias/norm/CLS/positional embedding khỏi weight decay; warmup/cosine theo iteration; Mixup/CutMix, label smoothing, clipping, AMP khi CUDA. Chọn best trên val Top-1. Quick chạy tối đa hai epoch, hai batch mỗi tập; thiếu cache thì cảnh báo và dùng dữ liệu giả. Quick có tên riêng; train thật thiếu cache phải dừng. Chặn ghi đè lần chạy có sẵn khi không có resume. Resume dùng cùng lịch/cấu hình, khôi phục optimizer/scheduler/scaler và lịch sử, không lặp CSV.
- **Kiểm tra:** test soft labels và CutMix theo diện tích thật; learning rate đầu/cuối và resume sau warmup; lỗi cấu hình/đầu vào; CPU quick cho hai model; fake cache chỉ có train/val để chứng minh không đọc test; checkpoint round-trip; lỗi ghi không phá file cũ; hai seed tách biệt; CUDA quick batch 64 đo VRAM và checkpoint scaler. Chạy toàn bộ `python -m pytest -q -W error` trong `.venv`.
- **Bàn giao:** ghi lệnh/kết quả thực tế ở tài liệu và JSON; chuẩn bị nội dung PR theo mẫu, chưa commit/push và chưa tự đánh dấu Hoàn thành. Tạo Issue/PR và cập nhật Projects khi có quyền GitHub.

## Bằng chứng

- Toàn repo: 72 passed, gồm 20 test train, với cảnh báo là lỗi. JUnit lưu nội bộ tại `.git/codex/task006_pytest.xml`.
- ViT và CNN mặc định chạy CPU/CUDA quick batch 64, có checkpoint best/last nạp được bằng weights_only, CSV và ảnh đường cong. GPU: RTX 5060 Laptop 8GB, PyTorch 2.11.0+cu128.
- [task006_training_checks.json](../../outputs/results/task006_training_checks.json), [hướng dẫn và giải thích](../06_training.md).
