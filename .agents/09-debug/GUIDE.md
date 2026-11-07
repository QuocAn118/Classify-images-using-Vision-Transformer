# 09 — Debug: tìm nguyên nhân và sửa lỗi

## Mục tiêu và đầu vào
Dựa trên bằng chứng để sửa nguyên nhân, rồi chứng minh lỗi được xử lý. Dùng lỗi phát hiện khi Review/Run/Test hoặc báo cáo người dùng.

## Thông tin cần thu thập
- **Expected behavior:** điều đáng lẽ xảy ra.
- **Actual behavior:** điều thực tế xảy ra.
- **Error message:** log, exception hoặc thông báo chính xác liên quan.
- **Relevant code:** file, hàm, bên gọi và cấu hình liên quan.
- **Environment:** runtime, phiên bản, hệ điều hành/dịch vụ khi ảnh hưởng lỗi.
- **Recent changes:** diff hoặc thay đổi gần đây có khả năng liên quan.

Tự đọc thông tin có sẵn trước khi hỏi. Thêm bước tái hiện và input lỗi khi có thể; không yêu cầu người dùng cung cấp lại dữ liệu đã thấy.

## Các bước thực hiện
1. Tái hiện lỗi bằng một ca nhỏ hoặc chạy lại test thất bại. Nếu chưa tái hiện được, ghi rõ điều kiện và khác biệt môi trường.
2. Xác định vị trí sai đầu tiên trong luồng, không chỉ vị trí hiển thị lỗi cuối cùng.
3. Đưa ra giả thuyết từ code/log/diff; chọn kiểm tra có thể xác nhận hoặc bác bỏ giả thuyết.
4. Thu hẹp nguyên nhân; tránh thay nhiều phần cùng lúc khiến không biết thay đổi nào có tác dụng.
5. Sửa trong phạm vi cần thiết, giữ contracts và hành vi không chịu ảnh hưởng.
6. Review bản sửa, chạy lại ca tái hiện và checks liên quan. Thêm regression test nếu có lợi ích thực tế.
7. Nếu lỗi còn lặp, cập nhật giả thuyết từ bằng chứng mới. Không lặp vô hạn cùng một cách sửa.
8. Nếu thiếu điều kiện bên ngoài, ghi rõ tiến độ và điều kiện còn thiếu; hỏi đúng thông tin cần để tiếp tục.

## Đầu ra cần có
Nguyên nhân có bằng chứng; file/hành vi đã sửa; ca tái hiện trước/sau; kết quả kiểm chứng; phần chưa xác định nếu còn.

## Điều kiện quay lại quy trình
- Ca lỗi đã được kiểm tra lại và cho kết quả mong đợi.
- Kiểm tra liên quan đạt hoặc giới hạn được ghi rõ.
- Quay lại Review/Run/Test phù hợp; chưa xác minh đủ thì chưa báo sửa xong.

## Prompt mẫu
```text
Dùng $vibe-coding để debug:
Expected behavior: ...
Actual behavior: ...
Error message/log: ...
Relevant code: ...
Environment: ...
Recent changes: ...
Các bước tái hiện: ...
Xác minh nguyên nhân, sửa phạm vi cần thiết và kiểm tra lại.
```
