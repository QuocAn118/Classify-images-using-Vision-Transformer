# 07 — Run: chạy code thực tế

## Mục tiêu và đầu vào
Chứng minh ứng dụng/module chạy được trong môi trường cụ thể. Dùng scripts và hướng dẫn thật của repo, cấu hình môi trường và ca sử dụng cơ bản.

## Các bước thực hiện
1. Xác định môi trường mục tiêu: runtime, phiên bản, working directory, dependencies và dịch vụ liên quan.
2. Đọc README, manifest và scripts để chọn đúng lệnh build/start hoặc lệnh chạy module. Không đoán rằng mọi project dùng cùng một lệnh.
3. Chuẩn bị điều kiện cần thiết trong phạm vi được giao. Nếu thiếu dữ liệu, cấu hình hoặc dịch vụ không thể tự cung cấp, ghi rõ điều kiện còn thiếu.
4. Chạy build khi project cần build, rồi chạy ứng dụng/module theo cách dự kiến.
5. Quan sát exit code, logs hoặc trạng thái ứng dụng; việc process còn chạy không tự chứng minh ứng dụng hoạt động.
6. Thực hiện một luồng cơ bản với input hợp lệ, kiểm tra output thực tế. Với giao diện, kiểm tra thao tác và kết quả hiển thị liên quan.
7. Có lỗi: ghi lệnh, môi trường, expected/actual và log liên quan, chuyển Debug.
8. Chạy được: chuyển Test để kiểm chứng phạm vi hành vi rộng hơn.

## Đầu ra cần có
```text
Environment:
Command / Entry point:
Input / Action:
Observed output:
Status / Exit code:
Missing conditions nếu có:
```

Không ghi giá trị bí mật vào báo cáo. Ghi trạng thái thiếu cấu hình mà không sao chép credential.

## Điều kiện chuyển bước
- Có bằng chứng chạy thực tế, không chỉ kết quả đọc code.
- Luồng cơ bản cho output mong đợi trong môi trường đã nêu.
- Nếu chưa chạy được, báo phần chưa xác minh; không đánh dấu Run pass.

## Prompt mẫu
```text
Dùng $vibe-coding để chạy module/ứng dụng vừa thay đổi.
Lấy lệnh và điều kiện chạy từ repo, kiểm tra một luồng cơ bản.
Ghi kết quả thực tế; nếu lỗi thì chuyển Debug, nếu đạt thì Test.
```
