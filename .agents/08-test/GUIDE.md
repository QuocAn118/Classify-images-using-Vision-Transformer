# 08 — Test: kiểm chứng hành vi

## Mục tiêu và đầu vào
Xác minh code đáp ứng tiêu chí và không làm hỏng hành vi liên quan. Dùng Describe, kết quả Run, test suite hiện có và contracts.

## Các bước thực hiện
1. Lập danh sách tiêu chí chấp nhận và gắn mỗi tiêu chí với cách kiểm chứng.
2. Ưu tiên tests sẵn có của phần bị sửa. Thêm hoặc cập nhật test khi cần chứng minh hành vi mới hoặc phòng lỗi tái diễn.
3. Chọn ca có ý nghĩa: luồng đúng; input lỗi/ca biên liên quan; tích hợp giữa các modules khi contract đổi.
4. Dùng kết quả quan sát được làm assertion. Tránh test chỉ khớp tên hàm, câu chữ hoặc lặp lại công thức implementation.
5. Chạy kiểm tra có phạm vi phù hợp. Bao gồm lint/typecheck/build khi repo yêu cầu hoặc thay đổi ảnh hưởng các kiểm tra này.
6. Phân biệt pass, fail và chưa chạy. Nếu có lỗi sẵn có hoặc môi trường thiếu, xác định bằng chứng trước khi kết luận lỗi không liên quan.
7. Test fail: chuyển Debug, sửa và chạy lại test thất bại cùng kiểm tra chịu ảnh hưởng.
8. Khi kiểm tra phù hợp đã pass, chỉ mở rộng/chạy lại nếu thay đổi mới, failure hoặc rủi ro còn mở đòi hỏi.

## Cách chọn kiểm tra tối thiểu
Phần “Minimum Tests” trong ảnh chưa có nội dung. Các lựa chọn dưới đây là hướng dẫn thực hành bổ sung, không phải bộ test bắt buộc chép từ ghi chú:
- Thay đổi logic: kiểm tra kết quả đúng và trường hợp lỗi/biên liên quan.
- Thay đổi interface/tích hợp: kiểm tra contract và luồng qua các thành phần chịu ảnh hưởng.
- Thay đổi giao diện: kiểm tra tương tác và kết quả hiển thị liên quan.
- Sửa tài liệu/định dạng nhỏ: kiểm tra nội dung hoặc hiển thị phù hợp; không thêm unit test máy móc.

## Đầu ra cần có
| Tiêu chí / hành vi | Cách kiểm tra | Kết quả | Giới hạn |
| --- | --- | --- | --- |
| Tiêu chí của nhiệm vụ | Test/lệnh/thao tác thực tế | Pass / Fail / Chưa chạy | Phần chưa bao phủ nếu có |

Ghi đúng lệnh đã chạy và kết quả; không báo “mọi thứ đều ổn” từ một kiểm tra hẹp.

## Điều kiện chuyển bước
- Những kiểm tra phù hợp với phần việc đã đạt.
- Failure có liên quan đã được sửa; giới hạn môi trường còn lại được nêu rõ.
- Cần cải thiện cấu trúc: sang Refactor; không cần: có thể chốt phần việc theo phạm vi được giao.

## Prompt mẫu
```text
Dùng $vibe-coding để kiểm chứng thay đổi theo tiêu chí chấp nhận.
Chạy tests/checks phù hợp, thêm test hành vi khi cần.
Báo lệnh thực tế, kết quả và giới hạn; xử lý failure liên quan.
```
