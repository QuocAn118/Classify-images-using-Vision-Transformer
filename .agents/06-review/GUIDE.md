# 06 — Review: kiểm tra code và giả định

## Mục tiêu và đầu vào
Đánh giá thay đổi so với Describe trước khi tin kết quả AI. Dùng diff, contracts, tiêu chí chấp nhận và code gọi module.

## Các bước thực hiện
1. Xem danh sách file và diff; phát hiện thay đổi ngoài phạm vi, file sinh tự động hoặc sửa nhầm.
2. Theo luồng input → xử lý → output để kiểm tra code có đáp ứng từng tiêu chí hay không.
3. Kiểm tra contracts: tên, kiểu dữ liệu, cấu trúc trả về, hành vi lỗi và tương thích với bên gọi.
4. Xác minh các giả định của AI: API/hàm có tồn tại, dependency đã khai báo, đường dẫn đúng, cấu hình khớp môi trường.
5. Xem nhánh lỗi và ca biên liên quan trực tiếp đến nhiệm vụ; kiểm tra thiếu/không hợp lệ/trùng lặp khi có ý nghĩa với tính năng.
6. Đọc test để xem có kiểm tra kết quả mong đợi hay chỉ phản chiếu implementation.
7. Sửa vấn đề đã có bằng chứng. Nếu không rõ nguyên nhân, chuyển Debug; nếu không có lỗi chặn, chuyển Run.
8. Ghi những điều review chưa chứng minh được để kiểm tra khi chạy và test.

## Đầu ra cần có
- Kết luận về phạm vi diff và các tiêu chí được code xử lý.
- Vấn đề phát hiện, cách sửa hoặc câu hỏi còn mở.
- Danh sách hành vi cần xác minh thực tế ở Run/Test.

Review bằng mắt không thay thế bằng chứng runtime hoặc test. Không coi nhận xét tự tin của AI là kết quả xác minh.

## Điều kiện chuyển bước
- Không còn lỗi review đã biết ngăn chạy hoặc làm sai hành vi cốt lõi.
- Các giả định chưa kiểm chứng được ghi rõ.
- Chưa gọi module hoàn thành chỉ vì diff đã review.

## Prompt mẫu
```text
Dùng $vibe-coding để review thay đổi của nhiệm vụ hiện tại.
Đối chiếu với tiêu chí chấp nhận, contracts và code bên gọi.
Xác minh giả định do AI đưa ra, sửa vấn đề có bằng chứng,
rồi tiếp tục Run/Test trong phạm vi được giao.
```
