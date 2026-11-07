# Breakdown và tiến độ

Chia theo kết quả có thể hiểu và kiểm tra. Trạng thái: Chưa bắt đầu → Đang làm → Đã triển khai, chưa xác minh → Hoàn thành. Dùng "Bị chặn" kèm nguyên nhân nếu thiếu điều kiện. AI báo xong chưa đủ để chuyển sang Hoàn thành.

## Phân công

| Thành viên | Vai trò | Phần báo cáo (mục 15 spec) |
|---|---|---|
| TV1 | Trưởng nhóm, dữ liệu, tài liệu | 1, 2, 8, 9 |
| TV2 | ViT và attention | 3 (ViT), 6 |
| TV3 | CNN, đo FLOPs/MACs | 3 (CNN), 6 (Grad-CAM nếu có) |
| TV4 | Huấn luyện | 4 |
| TV5 | Đánh giá, demo, ghép báo cáo | 5, 7, 10 |

Tên thật sẽ thay cho TV1-TV5 khi nhóm chốt. TV4 nên là thành viên có máy GPU, vì phụ trách train và quản lý checkpoint.

## Danh sách

| Mã | Đầu việc | Phụ trách | Yêu cầu | Phụ thuộc | Trạng thái | Bằng chứng |
|---|---|---|---|---|---|---|
| TASK-000 | Hoàn thiện `docs/` | TV1 | Quy trình `.agents/` | Không | Đã triển khai, chưa xác minh | Chờ nhóm đọc |
| TASK-014 | Nộp mẫu đăng ký (mục 21 spec) | TV1 | Đề | Nhóm chốt TV | Chưa bắt đầu | Chưa có |
| TASK-001 | Khung repo và tiện ích dùng chung | TV1 | AC-013, một phần AC-008 | TASK-000 | Chưa bắt đầu | Chưa có |
| TASK-002 | Chuẩn bị dữ liệu, chia tập, xuất mảng cache | TV1 | FR-001 | TASK-001, có file dữ liệu | Chưa bắt đầu | Chưa có |
| TASK-003 | DataLoader đọc mảng cache, augmentation | TV1 | FR-001 | TASK-002 | Chưa bắt đầu | Chưa có |
| TASK-004 | ViT và test | TV2 | FR-002 | TASK-001 | Chưa bắt đầu | Chưa có |
| TASK-005 | CNN và `match_param_count` | TV3 | FR-003 | TASK-004 | Chưa bắt đầu | Chưa có |
| TASK-006 | Vòng lặp train, `--quick`, `--resume` | TV4 | FR-004 | TASK-001, 003, 004, 005 | Chưa bắt đầu | Chưa có |
| TASK-007 | Đánh giá và phân tích lỗi | TV5 | FR-005 | TASK-006 | Chưa bắt đầu | Chưa có |
| TASK-008 | Trực quan hóa attention | TV2 | FR-006 | TASK-006 | Chưa bắt đầu | Chưa có |
| TASK-009 | Bảng so sánh | TV5 | FR-007 | TASK-007 | Chưa bắt đầu | Chưa có |
| TASK-010 | Demo | TV5 | FR-008 | TASK-006 | Chưa bắt đầu | Chưa có |
| TASK-011 | Train thật ViT và CNN | TV4 | FR-004 | TASK-006, máy GPU của thành viên sẵn sàng | Chưa bắt đầu | Chưa có |
| TASK-012 | Đánh giá test cuối và báo cáo | TV5, cả nhóm | FR-005, 007, 009 | TASK-011 | Chưa bắt đầu | Chưa có |
| TASK-013 | Phần làm thêm theo thứ tự mục 20 spec | Theo phần | Không bắt buộc | TASK-011 | Chưa bắt đầu | Chưa có |

**Điều kiện bắt đầu code:** Chỉ bắt đầu TASK-001 và các đầu việc code khác sau khi nhóm duyệt `docs/`. Bản thử đầu của TASK-001 viết sai thứ tự nên đã bị xóa.

**Ghi chú TASK-013:** Thứ tự cắt khi trễ: CNN thứ hai có FLOPs xấp xỉ ViT, rồi ablation, rồi 3 seed, rồi Grad-CAM, cuối cùng mới đến đo FLOPs/MACs (TV3 phụ trách). Thí nghiệm SGD được cắt cùng lúc với CNN thứ hai; attention theo head và layer được cắt cùng lúc với Grad-CAM. Giữ nguyên bộ lõi: ViT, CNN, attention, demo, báo cáo.

## Mốc và lịch

| Mốc | Kết quả trình diễn được | Đầu việc | Hạn |
|---|---|---|---|
| M0 | `docs/` được nhóm duyệt, đã nộp mẫu đăng ký | 000, 014 | 8/11 |
| M1 | Khung repo và hợp đồng sẵn sàng | 001 | 8/11 |
| M2 | `--quick` chạy thông từ dữ liệu đến checkpoint | 002-006 | 10/11 |
| M3 | Có checkpoint thật, đủ công cụ đánh giá và demo | 007-011 | 14/11 |
| M4 | Có số cuối trên test, dừng mọi thí nghiệm | 012, 013 | 16/11 |
| M5 | Báo cáo khớp số liệu, nộp bài | 012 | 19/11 |

20/11 để dự phòng. Quy tắc cắt việc khi trễ ở mục 20 của spec.

## Chi tiết đầu việc tiếp theo

- **Mã:** TASK-014
- **Mục tiêu:** Giảng viên nhận được mẫu đăng ký đủ 10 mục.
- **Phạm vi thay đổi:** Điền quyền sử dụng dữ liệu, sửa nháp nếu cần.
- **Phần cần đọc:** Mục 21 của `AGENT_SPEC_ViT_TinyImageNet.md`.
- **Ngoài phạm vi:** Code.
- **Phụ thuộc:** Nhóm chốt ai là TV nào.
- **Đầu ra:** Mẫu đã nộp.
- **Tiêu chí đạt:** Đủ 10 mục và đã nộp đúng nơi giảng viên quy định.
- **Cách kiểm tra:** Giảng viên xác nhận hoặc có bản đã nộp.
- **Người xem kết quả:** Cả nhóm.

## Giao việc cho AI
Đọc `AGENTS.md` và tài liệu liên quan đến TASK-[mã].
Khảo sát code liên quan; tìm phần có thể tái sử dụng.
Nêu phương án và giả định trước khi thực hiện thay đổi đáng kể.
Triển khai trong phạm vi đã chốt, chạy kiểm tra phù hợp.
Báo thay đổi, bằng chứng và phần chưa xác minh; cập nhật tiến độ thật.
