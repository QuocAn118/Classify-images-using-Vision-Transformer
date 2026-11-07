# Quy tắc làm việc trong repo

Áp dụng cho cả thành viên nhóm và AI coding agent.

## Đọc trước khi làm

1. [docs/04_BREAKDOWN.md](docs/04_BREAKDOWN.md): đầu việc và trạng thái hiện tại.
2. [docs/07_WORK_LOG.md](docs/07_WORK_LOG.md): bản ghi mới nhất.
3. Phần liên quan trong [docs/02_REQUIREMENTS.md](docs/02_REQUIREMENTS.md) và [docs/03_DESIGN.md](docs/03_DESIGN.md).
4. Hướng dẫn của bước đang làm trong [.agents/](.agents/).

## Quy trình

Đi theo thứ tự trong `.agents/`: Define, Design, Plan, rồi với từng đầu việc là Describe, Generate, Review, Run, Test, Debug và Refactor khi cần, Commit, Explain, Documentation, Definition of Done.

**Chưa được viết code khi nhóm chưa duyệt `docs/`.** Hiện `docs/` chưa được duyệt.

Với đầu việc nhỏ, một dòng bằng chứng trong `docs/06_VERIFICATION.md` là đủ; không cần điền đủ mẫu dài. Ưu tiên thời gian cho train và báo cáo.

## Quy tắc bắt buộc

- Mỗi lần chỉ làm một đầu việc trong `docs/04_BREAKDOWN.md`, không tự mở rộng phạm vi.
- Muốn đổi hợp đồng dùng chung trong `docs/03_DESIGN.md` thì sửa tài liệu và báo cả nhóm trước.
- Không dùng tập test để chọn siêu tham số hay checkpoint.
- Không bịa số liệu. Số trong báo cáo phải lấy từ file kết quả; chưa có thì ghi "chưa có".
- Không commit dữ liệu, checkpoint, `kaggle.json` hay bất kỳ bí mật nào.
- AI báo xong chưa đủ để đánh dấu Hoàn thành: phải có bằng chứng trong `docs/06_VERIFICATION.md` và người phụ trách đã xem.

## Git

- Giai đoạn tài liệu: làm thẳng trên `main`.
- Từ TASK-001 trở đi, khi 5 người code song song: mỗi người làm trên nhánh riêng rồi mở PR gộp vào `main`, TV1 là người duyệt; PR của chính TV1 do TV4 duyệt.
- Không dùng `git push --force` lên nhánh chung.
- Commit message mô tả kết quả cụ thể, không thêm dòng `Co-Authored-By`.
- AI chỉ commit hoặc push khi được yêu cầu.

## Sau mỗi buổi

- Cập nhật trạng thái thật trong `docs/04_BREAKDOWN.md`.
- Thêm bản ghi vào `docs/07_WORK_LOG.md`.
- Ghi công cụ AI đã dùng vào `AI_Usage.md`.
