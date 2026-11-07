# Phân loại ảnh Tiny ImageNet bằng Vision Transformer

Đồ án môn Học sâu, đề số 9. Nhóm tự cài ViT, so sánh với một CNN có cùng số tham số và trực quan hóa attention.

> **Trạng thái:** đang ở giai đoạn tài liệu, chờ nhóm duyệt `docs/`. Repo chưa có code, dữ liệu hay kết quả.

## Bài toán

Phân loại ảnh 64x64 vào 200 lớp. Dự án trả lời hai câu hỏi: với cùng số tham số, ViT so với CNN thế nào trên tập dữ liệu nhỏ, và ViT nhìn vào vùng nào của ảnh khi dự đoán.

## Tính năng dự kiến

- ViT tự cài bằng PyTorch (patch embedding + Transformer encoder).
- ResNet nhỏ có số tham số chênh không quá 5% so với ViT.
- Bảng so sánh Top-1, Top-5, số tham số, thời gian train và tốc độ inference.
- Hình CLS attention và attention rollout.
- Demo Gradio: tải ảnh lên, xem Top-5 và ảnh attention.

## Kiến trúc

Xem sơ đồ, thành phần và các hợp đồng dùng chung tại [docs/03_DESIGN.md](docs/03_DESIGN.md).

## Cài đặt và chạy

Chưa có. Lệnh dự kiến nằm trong [docs/05_TOOLS.md](docs/05_TOOLS.md) và sẽ được đưa vào đây sau khi đã chạy thử thật.

## Tài liệu

| File | Nội dung |
|---|---|
| [Project_description.md](Project_description.md) | Mục lục Define, Design, Plan |
| [docs/](docs/) | Đặc tả, thiết kế, phân công, kiểm chứng, nhật ký |
| [AGENT_SPEC_ViT_TinyImageNet.md](AGENT_SPEC_ViT_TinyImageNet.md) | Yêu cầu kỹ thuật chi tiết, nháp mẫu đăng ký |
| [AGENTS.md](AGENTS.md) | Quy tắc cho người và AI khi làm việc trong repo |
| [AI_Usage.md](AI_Usage.md) | Ghi nhận việc dùng AI |
| [.agents/](.agents/) | Quy trình 14 bước và mẫu tài liệu |
