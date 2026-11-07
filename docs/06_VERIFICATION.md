# Kiểm chứng và debug

Kết quả: Đạt / Không đạt / Chưa xác minh / Không áp dụng (nêu lý do). Mỗi đầu việc có một bản ghi. Không đưa bí mật vào bằng chứng.

**Hiện trạng:** Chưa có bản ghi kiểm chứng nào, vì repo chưa có code. Bản thử đầu của TASK-001 đã bị xóa nên kết quả chạy của nó không được tính là bằng chứng.

## Kiểm tra cần làm khi có code

| Kiểm tra | Mong đợi | Liên quan |
|---|---|---|
| Test fail trước khi có code | Fail vì chưa có chức năng | Quy trình TDD |
| Config thiếu khóa | Báo lỗi nêu tên khóa | AC-013 |
| Train bị ngắt rồi resume, dùng AdamW + warmup + cosine | Tiếp tục từ epoch k+1, log không trùng dòng, lr schedule khớp với chạy liền mạch (chênh không quá 1e-8), `val_loss` ở epoch k+1 chênh không quá 10% so với epoch k (không đòi trọng số giống hệt, vì shuffle, augmentation và GPU không tất định) | AC-008 |
| Phiên bị ngắt lúc đang lưu checkpoint | Checkpoint cũ không hỏng | AC-008, DEC-005 |
| Nạp checkpoint bằng `weights_only=True` | Nạp được, có đủ `scaler` và `class_names`; checkpoint chỉ chứa tensor, dict, list, số, chuỗi và `None` | Hợp đồng checkpoint |
| Chạy hai seed khác nhau | Log, checkpoint và kết quả nằm ở hai tên khác nhau, không ghi đè | Tên lần chạy |
| `--quick` khi chưa có cache; train thật khi chưa có cache | `--quick` dùng dữ liệu giả và cảnh báo; train thật báo lỗi | AC-007 |
| Demo trên máy không có bộ dữ liệu | Hiện đúng tên lớp, dùng đúng mean/std từ checkpoint | AC-012 |
| JSON kết quả | Có đủ khóa kể cả `macs`, `peak_vram_mb`; bảng so sánh lấy được cột FLOPs/MACs | AC-011 |
| Hai nhánh attention ở `model.eval()` | Logits hai nhánh chênh tuyệt đối tối đa 1e-4 | AC-005 |
| Cố tình làm hỏng code | Có test fail | Đánh giá chất lượng test |
| `.gitignore` | Chặn dữ liệu, checkpoint, `kaggle.json`; không chặn `outputs/logs`, `src/`, `.agents/`. Kiểm tra từng đường dẫn | Bảo vệ dữ liệu |
| Môi trường train | `--quick` chạy được trên máy GPU của thành viên, xác nhận đang dùng CUDA | FR-004 |
| VRAM đỉnh (đo khi làm TASK-006) | ViT và CNN ở batch 64 đều không lỗi hết bộ nhớ trên 6GB; nếu lỗi thì dùng gradient accumulation hoặc giảm batch còn 32 với cả hai mô hình | FR-004 |

## Mẫu bản ghi
- Mã: VERIFY-001
- Đầu việc / yêu cầu / tiêu chí: [TASK / FR / AC]
- Ngày, môi trường và phiên bản code: [cần điền]
- Người thực hiện / người xem kết quả: [cần điền]

| Kiểm tra | Lệnh hoặc thao tác thật | Mong đợi | Quan sát thực tế | Kết quả / bằng chứng |
|---|---|---|---|---|
| Luồng bình thường | [cần điền] | [cần điền] | [chưa chạy] | Chưa xác minh |
| Lỗi / trường hợp biên phù hợp | [cần điền] | [cần điền] | [chưa chạy] | Chưa xác minh |
| Code và thiết kế | [diff / đường dẫn / quyết định] | [cần điền] | [chưa xem] | Chưa xác minh |
| Chức năng liên quan có thể bị ảnh hưởng | [cần điền nếu cần] | [cần điền] | [chưa chạy] | Chưa xác minh |

## Đánh giá code (dùng cho mỗi đầu việc)
- Logic có đáp ứng yêu cầu và xử lý lỗi liên quan?
- Có tuân theo thiết kế hoặc ghi nhận thay đổi thiết kế?
- Có tái sử dụng hợp lý và tránh tạo bản trùng?
- Có theo cách tổ chức, đặt tên và quy tắc của dự án?
- Có rủi ro dữ liệu, quyền truy cập hoặc hiệu năng liên quan thay đổi?

## Mẫu ghi lỗi
- Cách tái hiện: [cần điền]
- Kỳ vọng / thực tế: [cần điền]
- Nguyên nhân và bằng chứng: [cần điền]
- Bản sửa: [cần điền]
- Kiểm tra bản sửa và ảnh hưởng: [cần điền]

## Kết luận (mỗi bản ghi)
- Tiêu chí đã đạt: [cần điền]
- Chưa xác minh / hạn chế: [cần điền]
- Quyết định và việc tiếp theo: [cần điền]
