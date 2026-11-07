# 02 — Design: thiết kế giải pháp

## Mục tiêu và đầu vào
Chuyển Define thành giải pháp có cấu trúc, triển khai được. Dùng phạm vi, input/output, tiêu chí đánh giá, ràng buộc và kiến trúc hiện có.

## Các bước thực hiện
1. Đọc stack và quy ước repo. Với project mới, chọn công nghệ theo yêu cầu, giải thích lựa chọn ảnh hưởng lớn.
2. Chia hệ thống thành thành phần có trách nhiệm rõ: giao diện, nghiệp vụ, lưu trữ, tích hợp tùy bài toán.
3. Thiết kế models: dữ liệu, quan hệ và bất biến; với ML, bổ sung mô hình học máy, input/output và cách đánh giá liên quan.
4. Mô tả data flow từ input đến output, kể cả nhánh lỗi ảnh hưởng hành vi.
5. Định nghĩa interfaces/APIs: thao tác, cấu trúc input/output, lỗi và bên chịu trách nhiệm xử lý.
6. Đề xuất folder structure theo thành phần và quy ước repo. Không tạo thư mục trống chỉ để đủ một kiến trúc mẫu.
7. Ghi rủi ro thực tế: tích hợp chưa xác nhận, dữ liệu thiếu, tài nguyên hoặc hiệu năng ảnh hưởng thiết kế.
8. Cập nhật phần Design trong `Project_description.md`; nối thành phần quan trọng với yêu cầu nó đáp ứng.

## Đầu ra cần có
System architecture; models; folder structure; data flow; interfaces/APIs; key decisions và lý do; technical risks, ảnh hưởng và cách kiểm chứng.

Ví dụ contract: `createItem({name}) → {id, name}`; tên rỗng trả lỗi validation và không tạo bản ghi. Đây là ví dụ, không phải API bắt buộc.

## Điều kiện chuyển bước
- Tính năng chính có đường đi qua các thành phần rõ ràng.
- Contracts đủ cụ thể để modules tích hợp được.
- Lựa chọn chưa xác minh được đánh dấu, không trình bày giả định như kết quả đã thử.

## Prompt mẫu
```text
Dùng $vibe-coding để thiết kế giải pháp từ Define hiện có.
Đề xuất architecture, models, folder structure, data flow,
interfaces/APIs và technical risks. Cập nhật phần Design.
Giữ ràng buộc của project; chưa viết code.
```
