# 04 — Describe: mô tả một nhiệm vụ

## Mục tiêu và đầu vào
Biến một phần kế hoạch thành nhiệm vụ nhỏ, rõ, kiểm chứng được. Dùng module đã chọn, contracts, code liên quan và trạng thái hiện tại.

## Các bước thực hiện
1. Đọc code/tài liệu module, xác định hành vi hiện tại và phần cần đổi.
2. Viết mục tiêu của vòng triển khai bằng một câu cụ thể.
3. Nêu bối cảnh cần thiết: file, interfaces, dữ liệu mẫu, phụ thuộc; không đưa toàn repo vào prompt nếu không cần.
4. Định nghĩa input/output, hành vi mong đợi và trường hợp lỗi liên quan.
5. Giới hạn phạm vi: phần cần sửa, contracts cần giữ; không gộp nhiệm vụ độc lập.
6. Viết tiêu chí chấp nhận và cách kiểm tra. Dùng lệnh có thật trong repo nếu biết; không tự bịa lệnh.
7. Chia thành vòng nhỏ hơn nếu nhiệm vụ có nhiều mục tiêu tách biệt.

## Đầu ra cần có
**Bối cảnh rõ + phạm vi nhỏ + tiêu chí kiểm chứng.**
Một task brief gồm Context, Single task, Input/Output, Expected behavior, Constraints/Scope, Acceptance criteria và Verification.

## Điều kiện chuyển bước
- Quyết định được code cần sửa mà không đoán yêu cầu cốt lõi.
- Kết quả đủ nhỏ để review và test trong một vòng.
- Không yêu cầu người dùng điền lại mẫu nếu đã có đủ thông tin.

## Prompt mẫu
```text
Dùng $vibe-coding để triển khai một nhiệm vụ: ...
Bối cảnh/file liên quan: ...
Input/output và hành vi mong đợi: ...
Giới hạn phạm vi: ...
Tiêu chí chấp nhận: ...
Lệnh kiểm tra đã biết: ...
Review, chạy và kiểm chứng thay đổi trước khi báo kết quả.
```
