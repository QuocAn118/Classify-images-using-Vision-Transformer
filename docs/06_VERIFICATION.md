# Kiểm chứng và debug

Kết quả: Đạt / Không đạt / Chưa xác minh / Không áp dụng (nêu lý do). Mỗi đầu việc có một bản ghi. Không đưa bí mật vào bằng chứng.

**Hiện trạng:** Chưa có bản ghi kiểm chứng nào, vì repo chưa có code. Bản thử đầu của TASK-001 đã bị xóa nên kết quả chạy của nó không được tính là bằng chứng.

## Kiểm tra cần làm khi viết lại TASK-001

| Kiểm tra | Mong đợi | Liên quan |
|---|---|---|
| Test fail trước khi có code | Fail vì chưa có chức năng | Quy trình TDD |
| Config thiếu khóa | Báo lỗi nêu tên khóa | AC-013 |
| Train bị ngắt rồi resume, dùng AdamW + warmup + cosine | Trọng số và lr giống chạy liền mạch, log không trùng dòng | AC-008 |
| Phiên bị ngắt lúc đang lưu checkpoint | Checkpoint cũ không hỏng | AC-008, DEC-005 |
| Cố tình làm hỏng code | Có test fail | Đánh giá chất lượng test |
| `.gitignore` | Chặn dữ liệu, checkpoint, `kaggle.json`; không chặn `outputs/logs`, `src/`, `.agents/`. Kiểm tra từng đường dẫn | Bảo vệ dữ liệu |
| Môi trường train | Chạy được trên Kaggle hoặc Colab | FR-004 |

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
