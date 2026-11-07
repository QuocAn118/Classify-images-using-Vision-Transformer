# 01 — Define: xác định bài toán

## Mục tiêu và đầu vào
Hiểu cần xây gì, vì sao và cho ai trước khi chọn công nghệ. Đọc yêu cầu, bối cảnh sử dụng, tài liệu và repository hiện có.

## Các bước thực hiện
1. **What:** mô tả vấn đề và kết quả cần đạt bằng hành vi cụ thể; tách yêu cầu đã xác nhận khỏi giả định.
2. **Why:** xác định giá trị của giải pháp, khó khăn hiện tại và lý do cần tính năng này.
3. **When / Where / Which:** xác định tình huống sử dụng, nền tảng, nhóm người dùng và lựa chọn ảnh hưởng giải pháp.
4. **How ở mức yêu cầu:** xác định input/output và giới hạn; chưa chốt kỹ thuật trước khi hiểu bài toán.
5. Chọn tính năng phiên bản đầu và ghi phần ngoài phạm vi. Không tự mở rộng sản phẩm.
6. Ghi ràng buộc: công nghệ bắt buộc nếu có, môi trường, tài nguyên, thời gian, dữ liệu và tích hợp.
7. Viết tiêu chí đánh giá quan sát hoặc đo được; tránh chỉ nói “tốt”, “nhanh”, “dễ dùng”.
8. Ghi phần Define vào `Project_description.md`; nếu repo đã có tài liệu tương đương, cập nhật theo quy ước.

## Đầu ra cần có
Tên project; problem statement; target users; use cases; input/output; core features; out of scope; technical constraints; evaluation criteria; assumptions/open questions.

Ví dụ tiêu chí: “Nhập dữ liệu hợp lệ và nhấn Lưu thì bản ghi xuất hiện trong danh sách; thiếu tên thì hiển thị lỗi và không lưu.”

## Điều kiện chuyển bước
- Giải thích được bài toán, người dùng và kết quả mong đợi.
- Phạm vi đủ rõ để thiết kế; câu hỏi còn mở không chặn quyết định, hoặc được ghi rõ là điều kiện cần làm rõ.
- Chưa viết code ở bước này.

## Prompt mẫu
```text
Dùng $vibe-coding để thực hiện Define cho ý tưởng: ...
Bối cảnh sử dụng: ...
Ràng buộc đã biết: ...
Ghi phần Define trong Project_description.md. Chỉ hỏi điểm thiếu
ảnh hưởng đến phạm vi hoặc tiêu chí đánh giá. Chưa viết code.
```
