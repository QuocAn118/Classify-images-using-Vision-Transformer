# 12 — Explain code: hiểu code đang dùng

## Mục tiêu và đầu vào
Giúp người dùng hiểu hành vi, quyết định và phần code cần duy trì. Dùng implementation thật, diff, contracts và kết quả kiểm chứng.

## Các bước thực hiện
1. Mở đầu bằng kết quả: phần code này giải quyết yêu cầu nào và hành vi mới là gì.
2. Theo một input cụ thể qua entry point, xử lý chính, dữ liệu hoặc dịch vụ, đến output.
3. Chỉ ra file/hàm quan trọng và trách nhiệm của chúng; liên kết code khi có thể.
4. Giải thích quyết định ảnh hưởng bảo trì: vì sao đặt logic ở đây, vì sao dùng dependency này, vì sao chọn cách xử lý lỗi.
5. Nêu trường hợp lỗi/ca biên liên quan và cách code xử lý.
6. Nối tiêu chí chấp nhận với tests hoặc thao tác đã xác minh. Phân biệt hành vi mong đợi và kết quả thực tế đã quan sát.
7. Nêu giới hạn còn lại và nơi cần sửa nếu người dùng muốn mở rộng một tính năng liên quan.
8. Điều chỉnh độ sâu theo người dùng. Không giảng từng dòng, dùng thuật ngữ không giải thích hoặc chỉ dán lại toàn bộ code.

## Đầu ra cần có
```text
Code làm gì:
Luồng input → xử lý → output:
File/hàm chính:
Quyết định và lý do:
Kiểm chứng đã thực hiện:
Giới hạn/cách mở rộng liên quan:
```

Không suy đoán người dùng đã hiểu chỉ vì đã gửi giải thích. Khi người dùng hỏi lại, giải thích bằng ví dụ cụ thể ở phần họ cần.

## Điều kiện chuyển bước
- Giải thích khớp code hiện tại, không mô tả kế hoạch cũ.
- Những quyết định và luồng quan trọng được trình bày đủ để đọc/duy trì.
- Không bịa lý do hoặc nhận rằng code AI đúng khi chưa có kiểm chứng.

## Prompt mẫu
```text
Dùng $vibe-coding để giải thích module ... theo code hiện tại.
Đi theo một ví dụ input đến output, chỉ ra file/hàm chính,
quyết định thiết kế, cách xử lý lỗi và bằng chứng kiểm chứng.
Giải thích ở mức người mới học có thể theo dõi.
```
