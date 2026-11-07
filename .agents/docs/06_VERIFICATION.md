# Kiểm chứng và debug

## Mẫu bản ghi
- Mã: VERIFY-001
- Đầu việc / yêu cầu / tiêu chí: [TASK / FR / AC]
- Ngày, môi trường và phiên bản code: [cần điền]
- Người thực hiện / người xem kết quả: [cần điền]

| Kiểm tra | Lệnh hoặc thao tác thật | Mong đợi | Quan sát thực tế | Kết quả / bằng chứng |
| --- | --- | --- | --- | --- |
| Luồng bình thường | [cần điền] | [cần điền] | [chưa chạy] | Chưa xác minh |
| Lỗi / trường hợp biên phù hợp | [cần điền] | [cần điền] | [chưa chạy] | Chưa xác minh |
| Code và thiết kế | [diff / đường dẫn / quyết định] | [cần điền] | [chưa xem] | Chưa xác minh |
| Chức năng liên quan có thể bị ảnh hưởng | [cần điền nếu cần] | [cần điền] | [chưa chạy] | Chưa xác minh |

Kết quả: Đạt / Không đạt / Chưa xác minh / Không áp dụng (nêu lý do).
Bằng chứng: log ngắn, kết quả test, ảnh, hoặc bước thử có thể lặp lại. Không đưa bí mật vào bằng chứng.

## Đánh giá code
- Logic có đáp ứng yêu cầu và xử lý lỗi liên quan?
- Có tuân theo thiết kế hoặc ghi nhận thay đổi thiết kế?
- Có tái sử dụng hợp lý và tránh tạo bản trùng?
- Có theo cách tổ chức, đặt tên và quy tắc của dự án?
- Có rủi ro dữ liệu, quyền truy cập hoặc hiệu năng liên quan thay đổi?

## Nếu gặp lỗi
- Cách tái hiện: [cần điền]
- Kỳ vọng / thực tế: [cần điền]
- Nguyên nhân và bằng chứng: [cần điền]
- Bản sửa: [cần điền]
- Kiểm tra bản sửa và ảnh hưởng: [cần điền]

## Kết luận
- Tiêu chí đã đạt: [cần điền]
- Chưa xác minh / hạn chế: [cần điền]
- Quyết định và việc tiếp theo: [cần điền]
