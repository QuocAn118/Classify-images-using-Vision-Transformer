# 03 — Plan: modules và milestones

## Mục tiêu và đầu vào
Tạo thứ tự triển khai có thể kiểm chứng từ Define và Design. Kế hoạch phải đủ để bắt đầu nhiệm vụ tiếp theo, không cần đoán mọi thay đổi tương lai.

## Các bước thực hiện
1. Chia tính năng thành modules theo trách nhiệm hoặc luồng hành vi; mỗi module có input/output và tiêu chí hoàn thành.
2. Xác định phụ thuộc: contracts, dữ liệu hoặc thành phần cần từ module khác.
3. Ưu tiên kiểm chứng rủi ro ảnh hưởng lớn. Nếu cần thử nghiệm nhỏ, giới hạn câu hỏi thử nghiệm phải trả lời.
4. Gom modules thành milestones có kết quả chạy, trình diễn hoặc đánh giá được.
5. Với mỗi module, ghi nhiệm vụ, phạm vi file dự kiến, phụ thuộc và cách kiểm chứng. Chia nhỏ nếu một prompt ôm nhiều việc.
6. Ghi kế hoạch trong `Project_description.md` hoặc nơi quản lý kế hoạch hiện có.
7. Chọn nhiệm vụ đầu tiên. Cập nhật kế hoạch khi có phát hiện mới, không coi bản đầu là bất biến.

## Đầu ra cần có
| Module / milestone | Kết quả | Phụ thuộc | Cách kiểm chứng | Trạng thái |
| --- | --- | --- | --- | --- |
| Ví dụ: tạo và liệt kê bản ghi | Lưu và xem lại dữ liệu | Contract dữ liệu | Tạo → liệt kê; input lỗi | Chưa làm |

Thêm rủi ro còn mở và nhiệm vụ tiếp theo. Không ghi hoàn thành khi chưa có bằng chứng.

## Điều kiện chuyển bước
- Nhiệm vụ tiếp theo nhỏ, rõ và có tiêu chí kiểm chứng.
- Phụ thuộc sẵn sàng hoặc điều kiện còn thiếu được nêu rõ.
- Chỉ yêu cầu PLAN: bàn giao kế hoạch, dừng trước Generate. Đã giao triển khai: tiếp tục trong phạm vi được giao.

## Prompt mẫu
```text
Dùng $vibe-coding để chia project thành modules và milestones.
Nêu phụ thuộc, thứ tự triển khai, rủi ro và tiêu chí kiểm chứng.
Chỉ lập kế hoạch, chưa viết code.
```
