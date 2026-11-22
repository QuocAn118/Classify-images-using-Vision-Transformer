# Project description: ViT phân loại ảnh trên Tiny ImageNet

Đồ án môn Học sâu, đề số 9, nhóm 5 người, hạn nộp 2026-11-25 (đã gia hạn từ 2026-11-20). File này tóm tắt Define, Design, Plan; chi tiết nằm trong `docs/`, mỗi thứ chỉ viết một lần ở đó.

## Thứ tự đọc

Người mới đọc file này trước, rồi đọc `docs/` theo số:

1. `01_define.md`: bài toán, phạm vi, yêu cầu.
2. `02_architecture.md`: các thành phần ghép với nhau thế nào.
3. `03_plan.md`: ai làm gì, mốc nào.
4. `04_data.md` đến `08_demo.md`: từng thành phần theo luồng dữ liệu. Ai giữ phần nào thì đọc kỹ file đó.
5. `09_decisions.md`, `10_work_log.md`: tra cứu khi cần biết vì sao chọn một phương án, hoặc đã làm gì gần đây.

## Define
- **Bài toán:** Phân loại ảnh 64x64 vào 200 lớp Tiny ImageNet bằng Vision Transformer tự cài, so sánh với một CNN có số tham số chênh không quá 5%, và trực quan hóa attention.
- **Người dùng:** Sinh viên, người nghiên cứu thị giác máy tính, giảng viên chấm bài.
- **Phạm vi:** ViT, CNN cùng số tham số, attention, demo Gradio, phân tích lỗi. Ngoài phạm vi: ViT pretrained, deepfake, triển khai production.
- **Thành công khi:** Có Top-1, Top-5 trên test cho cả hai mô hình; tham số chênh không quá 5%; có hình attention cho ít nhất 12 ảnh.
- **Ràng buộc:** khoảng 10 ngày tính từ 15/11, một máy GPU 6GB VRAM, không dùng test để chọn cấu hình, không bịa số liệu.

Chi tiết, yêu cầu chức năng và giả định còn mở: [docs/01_define.md](docs/01_define.md).

## Design
- **Luồng:** Tiny ImageNet → chuẩn bị dữ liệu và cache → train ViT, CNN → checkpoint → đánh giá, attention, demo → bảng so sánh.
- **Mô hình:** ViT-small (patch 8, dim 256, depth 8, 6.436.296 tham số) và ResNet-small (6.476.808 tham số, chênh 0,63%); bằng chứng tại [docs/05_model.md](docs/05_model.md).
- **Huấn luyện:** AdamW, batch 64, lr 2,5e-4, 50 epoch (mức sàn), chọn checkpoint trên validation.

| Thành phần | Tài liệu | Người giữ |
|---|---|---|
| Kiến trúc tổng, config, môi trường | [docs/02_architecture.md](docs/02_architecture.md) | TV1 |
| Dữ liệu | [docs/04_data.md](docs/04_data.md) | TV1 |
| Mô hình | [docs/05_model.md](docs/05_model.md) | TV2, TV3 |
| Huấn luyện | [docs/06_training.md](docs/06_training.md) | TV4 |
| Đánh giá, attention, so sánh | [docs/07_evaluation.md](docs/07_evaluation.md) | TV5, TV2 |
| Demo | [docs/08_demo.md](docs/08_demo.md) | TV5 |
| Quyết định thiết kế | [docs/09_decisions.md](docs/09_decisions.md) | Cả nhóm |

## Plan
- **Mốc:** duyệt tài liệu và nộp mẫu đăng ký → khung repo → `--quick` chạy thông → train thật → số cuối trên test → nộp bài 24/11 (25/11 dự phòng).
- **Trạng thái:** TASK-001 đến TASK-011 đã gộp vào main; ViT/CNN train đủ 50 epoch; test Top-1 ViT 48,46%, CNN 59,03%; có bảng so sánh và demo Gradio. Còn TASK-012 (hoàn thiện báo cáo, nộp bài) và TASK-013 (tùy chọn).
- **Đầu việc tiếp theo:** TV1 review phần TV4; bàn giao checkpoint cho TASK-008 (TV2, attention) và các phần đánh giá/so sánh/demo của TV5. Chưa có kết quả test cuối hoặc link chia sẻ checkpoint. Chi tiết ở [docs/03_plan.md](docs/03_plan.md).

Phân công, danh sách đầu việc, thứ tự cắt việc và checklist nộp bài: [docs/03_plan.md](docs/03_plan.md). Nhật ký: [docs/10_work_log.md](docs/10_work_log.md).

Yêu cầu kỹ thuật đầy đủ và nháp mẫu đăng ký: [SPEC_ViT.md](SPEC_ViT.md).
