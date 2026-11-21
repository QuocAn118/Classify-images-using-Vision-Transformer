# Demo

**Người giữ:** TV5<br> **Đầu việc:** TASK-010. <br> **Code:** `app/demo.py`

## Thành phần làm gì
Giao diện Gradio chạy cục bộ trên CPU: tải một ảnh lên, xem Top-5 của ViT và CNN cùng ảnh attention rollout. Không cần bộ dữ liệu, chỉ cần checkpoint.

## Đầu vào
- Checkpoint ViT và CNN theo hợp đồng ở [06_training.md](06_training.md). Tên lớp lấy từ `class_names`, mean/std lấy từ `config` trong checkpoint.
- Mô hình gọi theo hợp đồng ở [05_model.md](05_model.md).

## FR-008: Demo
- **Người sử dụng:** Người xem demo, giảng viên.
- **Mục đích:** Thử mô hình trên một ảnh.
- **Đầu vào:** Checkpoint ViT và CNN, ảnh tải lên.
- **Luồng bình thường:** Tải ảnh, tự resize, hiển thị Top-5 của hai mô hình và ảnh attention rollout.
- **Quy tắc:** Chạy được trên CPU; có ảnh mẫu trong `app/examples/`.
- **Lỗi và biên:** Thiếu checkpoint hoặc file không phải ảnh thì báo lỗi dễ hiểu; ảnh xám hoặc có kênh alpha được chuyển về RGB.
- **Kết quả:** Giao diện Gradio trả kết quả.

## Tiêu chí nghiệm thu

| Mã | Điều kiện ban đầu | Thao tác | Kết quả mong đợi |
|---|---|---|---|
| AC-012 | Có checkpoint, CPU, máy không có bộ dữ liệu | Chạy `app/demo.py`, tải ảnh lên | Hiển thị Top-5 hai mô hình với đúng tên lớp, dùng đúng mean/std từ checkpoint, và ảnh attention |

## Cách chạy

| Lệnh | Điều kiện | Trạng thái |
|---|---|---|
| `python app/demo.py` | Có checkpoint, đã cài `gradio` | Đã có code |

Kiểm tra bằng trình duyệt: tải ảnh, đối chiếu Top-5 và ảnh attention.
