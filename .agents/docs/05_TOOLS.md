# Công cụ và môi trường

Điền từ dự án thật. Không sao chép lệnh mẫu rồi giả định dự án hỗ trợ.
Không ghi API key, mật khẩu hoặc token vào tài liệu.

## Công cụ
| Nhu cầu | Công cụ dự án dùng | Khi dùng | Cách kiểm tra |
| --- | --- | --- | --- |
| Tìm file / logic hiện có | [ví dụ: rg hoặc tìm kiếm IDE] | Trước khi tạo hoặc sửa | Đọc kết quả và code liên quan |
| Chỉnh code | [AI coding / IDE thực tế] | Khi yêu cầu và phạm vi đã rõ | Xem diff |
| Kiểm tra logic | [bộ test dự án] | Khi thay đổi hành vi / sửa lỗi | Kết quả và trường hợp được bao phủ |
| Kiểm tra UI | [trình duyệt / công cụ thực tế] | Khi sửa giao diện | Thử thao tác, đối chiếu thiết kế |
| Kiểm thử app thật (E2E) | [ví dụ: e2e (tester-army), Playwright, không áp dụng] | Trước khi báo xong một luồng người dùng | Test chạy trên app thật, có `expect`; xem `.e2e/report.json` |
| Tra tài liệu | [nguồn chính thức] | Khi chưa chắc API / phiên bản | Đối chiếu phiên bản đang dùng |
| Lưu phiên bản | Git nếu dự án dùng | Khi phần việc đã được kiểm tra | Xem diff và trạng thái trước commit |

## Lệnh thật
| Mục đích | Lệnh | Thư mục chạy | Điều kiện |
| --- | --- | --- | --- |
| Cài đặt | [cần điền] | [cần điền] | [cần điền] |
| Chạy | [cần điền] | [cần điền] | [cần điền] |
| Build / typecheck | [cần điền / không áp dụng] | [cần điền] | [cần điền] |
| Lint | [cần điền / không áp dụng] | [cần điền] | [cần điền] |
| Test liên quan | [cần điền] | [cần điền] | [cần điền] |
| Test E2E | [ví dụ: `npx e2e run`] | [cần điền] | [ví dụ: Node 24.8+; Windows chạy trong WSL; model qua `npx e2e login` hoặc biến môi trường] |

## Kiểm thử E2E bằng AI (tùy chọn)
Dùng khi dự án có web/mobile UI và cần AI tự kiểm tra app thật thay vì tự kết luận.
- Cài một lần cho dự án (cần đồng ý vì thêm devDependency): `npx e2e init`.
- Hướng dẫn cho AI: skill `qa`, mục "Using e2e". Tài liệu: https://e2e.tester.army/docs
- Không ghi API key vào tài liệu; chỉ ghi tên biến môi trường.

## Tối ưu thời gian và ngữ cảnh
- Đọc phần liên quan trước; mở rộng khi phát hiện phụ thuộc.
- Giao đầu việc đủ nhỏ để xem lại và kiểm tra.
- Tái sử dụng tài liệu và code; dẫn tới nội dung chi tiết thay vì chép lại.
- Chạy kiểm tra phù hợp thay đổi; không lặp bộ kiểm tra lớn khi chưa có lý do.
- Ghi lại kết quả có ý nghĩa để tiếp tục buổi sau.
- Chưa biết công cụ hoặc lệnh có hoạt động thì ghi là chưa xác minh.
