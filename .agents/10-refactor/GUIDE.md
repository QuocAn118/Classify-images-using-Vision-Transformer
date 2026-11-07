# 10 — Refactor: cải thiện cấu trúc code

## Mục tiêu và đầu vào
Làm code dễ hiểu và duy trì hơn, giữ hành vi đã xác minh. Dùng code đã Review/Run/Test, điểm khó hiểu cụ thể và contracts hiện có.

## Các bước thực hiện
1. Nêu vấn đề cấu trúc cụ thể: trách nhiệm trộn lẫn, lặp logic, tên khó hiểu hoặc phụ thuộc khó kiểm soát.
2. Xác định hành vi phải giữ và checks dùng để phát hiện thay đổi ngoài ý muốn.
3. Chọn cải tiến nhỏ phục vụ vấn đề đó. Không thay kiến trúc hoặc mở rộng tính năng chỉ vì đang refactor.
4. Tách hàm/thành phần, đổi tên hoặc giảm lặp khi giúp code rõ hơn; giữ public contracts trừ khi nhiệm vụ cho phép đổi.
5. Review diff để tìm thay đổi hành vi vô tình và ảnh hưởng bên gọi.
6. Chạy lại tests/checks chịu ảnh hưởng sau mỗi nhóm thay đổi có ý nghĩa.
7. Nếu hành vi đổi ngoài ý muốn, Debug và sửa trước khi chốt.
8. Cập nhật giải thích/tài liệu nếu vị trí code hoặc luồng xử lý thay đổi đáng kể.

## Đầu ra cần có
- Vấn đề cấu trúc đã xử lý và lý do.
- Thay đổi code nhỏ, review được.
- Bằng chứng hành vi cần giữ vẫn đạt sau refactor.

## Điều kiện chuyển bước
- Checks liên quan pass sau refactor.
- Không còn thay đổi hành vi vô tình đã biết.
- Nếu không có vấn đề cấu trúc cần xử lý, bỏ qua bước này; không refactor để đủ quy trình.

## Prompt mẫu
```text
Dùng $vibe-coding để refactor phần ... vì vấn đề cấu trúc ...
Giữ hành vi/contracts hiện có, giới hạn trong phạm vi liên quan.
Review diff và chạy lại kiểm tra chịu ảnh hưởng sau khi sửa.
```
