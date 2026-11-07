# 05 — Generate: triển khai code

## Mục tiêu và đầu vào
Viết code đáp ứng một nhiệm vụ đã Describe theo kiến trúc, contracts và quy ước hiện có.

## Các bước thực hiện
1. Kiểm tra Git và hướng dẫn repo trước khi sửa; nhận diện thay đổi có sẵn của người dùng.
2. Project mới chưa có Git: xác định đúng thư mục project rồi khởi tạo; không khởi tạo ở thư mục cha.
3. Đọc implementations, dependencies và scripts hiện có để tái sử dụng đúng quy ước.
4. Triển khai phần việc nhỏ đã chọn. Giữ contracts, hoặc cập nhật Design nếu bằng chứng cho thấy cần đổi trong phạm vi đã giao.
5. Xử lý input/output và lỗi liên quan đến tiêu chí chấp nhận. Không thêm tính năng ngoài nhiệm vụ.
6. Chỉ thêm dependency khi cần và phù hợp môi trường; kiểm tra API/phiên bản thực tế thay vì tin code AI sinh ra.
7. Khi phù hợp, thêm/cập nhật tests cho hành vi thay đổi. Giữ thay đổi có sẵn của người dùng.
8. Xem lại danh sách file sửa và chuyển sang Review; code được tạo chưa chứng minh là chạy đúng.

## Đầu ra cần có
- Code nhiệm vụ hiện tại và tests liên quan nếu cần.
- File chịu ảnh hưởng và lý do thay đổi.
- Giả định, thay đổi contract hoặc dependency mới cần review nếu có.

## Điều kiện chuyển bước
- Thay đổi đủ để so sánh với Describe.
- Không để nhiệm vụ khác chen vào diff.
- Chưa báo hoàn thành/test pass chỉ vì code trông hợp lý.

## Prompt mẫu
```text
Dùng $vibe-coding để viết code cho nhiệm vụ đã mô tả.
Theo quy ước repo và contracts hiện có, chỉ sửa phần liên quan.
Sau khi viết, tiếp tục Review → Run → Test.
```
