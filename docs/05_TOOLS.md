# Công cụ và môi trường

Chỉ ghi những gì đã có thật trong dự án. Không ghi API key, mật khẩu, token hay nội dung `kaggle.json` vào tài liệu.

## Môi trường đã kiểm tra

| Thành phần | Giá trị |
|---|---|
| Hệ điều hành | Windows 10 |
| Python | 3.13.9 |
| PyTorch | 2.9.1+cpu, không có GPU |
| Chưa cài trên máy này | `timm`, `gradio`, `thop`, `fvcore` |
| GPU để train | Kaggle hoặc Colab, chưa kiểm tra |

## Công cụ

| Nhu cầu | Công cụ dự án dùng | Khi dùng | Cách kiểm tra |
|---|---|---|---|
| Tìm file / logic hiện có | Tìm kiếm trong IDE, `rg` | Trước khi tạo hoặc sửa | Đọc kết quả và code liên quan |
| Chỉnh code | VS Code, Claude Code | Khi yêu cầu và phạm vi đã rõ | Xem diff |
| Kiểm tra logic | `pytest` | Khi thay đổi hành vi hoặc sửa lỗi | Kết quả và trường hợp được bao phủ |
| Kiểm tra UI | Trình duyệt mở demo Gradio | Khi sửa demo | Tải ảnh, đối chiếu Top-5 và ảnh attention (chưa có demo) |
| Kiểm thử app thật (E2E) | Không áp dụng | Demo nhỏ, kiểm tra thủ công là đủ | Không áp dụng |
| Train bằng GPU | Kaggle hoặc Colab | Khi đã qua `--quick` | Log CSV, checkpoint |
| Tra tài liệu | Tài liệu chính thức của PyTorch, torchvision, Gradio | Khi chưa chắc API hoặc phiên bản | Đối chiếu phiên bản đang dùng |
| Lưu phiên bản | Git, GitHub | Khi phần việc đã được kiểm tra | Xem diff và trạng thái trước commit |

## Lệnh thật

| Mục đích | Lệnh | Thư mục chạy | Điều kiện | Trạng thái |
|---|---|---|---|---|
| Cài đặt | `pip install -r requirements.txt` | Gốc repo | Có mạng | Chưa có code |
| Build / typecheck | Không áp dụng | | | |
| Lint | Không áp dụng, chưa cấu hình | | | |
| Test liên quan | `pytest` | Gốc repo | Đã cài dependency | Chưa có code |
| Test E2E | Không áp dụng | | | |
| Chuẩn bị dữ liệu | `python scripts/prepare_data.py` | Gốc repo | Có file dữ liệu | Chưa có code |
| Train | `python -m src.train --config configs/vit_small.yaml` | Gốc repo | Dữ liệu đã chuẩn bị, nên có GPU | Chưa có code |
| Đánh giá | `python -m src.evaluate` | Gốc repo | Có checkpoint | Chưa có code |
| Attention | `python -m src.attention` | Gốc repo | Có checkpoint ViT | Chưa có code |
| So sánh | `python -m src.compare` | Gốc repo | Có JSON kết quả | Chưa có code |
| Demo | `python app/demo.py` | Gốc repo | Có checkpoint | Chưa có code |

Các lệnh "Chưa có code" lấy từ spec, sẽ cập nhật sau khi chạy thật.

## Dữ liệu và bí mật

- `kaggle.json` không được commit; TASK-001 phải tạo `.gitignore` chặn file này, dữ liệu và checkpoint trước khi có ai tải dữ liệu vào repo.
- Dữ liệu và checkpoint không commit. Checkpoint lưu trên Google Drive hoặc Kaggle Dataset, link ghi trong README.

## Tối ưu thời gian và ngữ cảnh
- Đọc phần liên quan trước; mở rộng khi phát hiện phụ thuộc.
- Giao đầu việc đủ nhỏ để xem lại và kiểm tra.
- Chạy `--quick` trên CPU trước khi tốn giờ GPU.
- Lưu checkpoint thường xuyên vì phiên GPU có thể bị ngắt.
- Chưa biết công cụ hoặc lệnh có hoạt động thì ghi là chưa xác minh.
