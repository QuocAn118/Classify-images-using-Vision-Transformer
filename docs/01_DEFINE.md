# Define

**Nguồn đã xác nhận:** đề số 9 và mẫu đăng ký của giảng viên (ảnh chụp sheet môn học), hạn nộp do nhóm cung cấp. Nội dung còn lại là đề xuất của nhóm, xem bảng giả định cuối file.

## What — Làm gì?
- **Bài toán:** Phân loại ảnh vào 200 lớp bằng Vision Transformer (patch embedding + Transformer encoder).
- **Sản phẩm và người sử dụng:** Mô hình đã huấn luyện, bảng so sánh, hình attention, demo và báo cáo; dành cho sinh viên, người nghiên cứu thị giác máy tính và giảng viên chấm bài.
- **Chức năng chính:**
  - Huấn luyện ViT và một CNN có cùng số tham số trên cùng dữ liệu.
  - So sánh hai mô hình bằng các chỉ số đo được.
  - Trực quan hóa attention của ViT.
  - Demo: tải một ảnh lên và xem kết quả dự đoán.

## Why — Vì sao?
- **Vấn đề của cách làm hiện tại:** ViT thường cần nhiều dữ liệu. Các so sánh hay dùng mô hình khác cỡ nên khó công bằng, và khó biết mô hình dựa vào vùng nào của ảnh.
- **Giá trị mong muốn:** Có bằng chứng đo được về ViT và CNN khi cùng ngân sách tham số, trên ảnh nhỏ và dữ liệu ít.
- **Dấu hiệu hoặc chỉ số thành công:**
  - Số tham số hai mô hình chênh không quá 5%.
  - Có Top-1 và Top-5 trên tập test cho cả hai mô hình.
  - Có hình attention cho ít nhất 12 ảnh test.
  - Mức tham khảo, không phải điều kiện đạt: ViT >= 40% và CNN >= 50% Top-1.

## When — Khi nào?
- **Tình huống/kích hoạt:** Người dùng chạy lệnh train, đánh giá hoặc mở demo khi cần kết quả; giảng viên chạy lại theo README khi chấm.
- **Thời hạn và mốc:** Hạn nộp 2026-11-20, nhóm đặt mục tiêu nộp 2026-11-19. Các mốc ở [04_BREAKDOWN.md](04_BREAKDOWN.md).

## Where — Ở đâu?
- **Nơi dùng, thiết bị, môi trường:** Phát triển trên máy cá nhân (máy của TV viết tài liệu chỉ có CPU); train trên máy có GPU 6GB VRAM của một thành viên khác trong nhóm, máy rảnh trong thời gian train; Kaggle hoặc Colab là phương án dự phòng.
- **Môi trường demo / triển khai:** Demo Gradio chạy cục bộ trên CPU. Không triển khai production.

## Which — Chọn gì, giới hạn gì?
- **Phạm vi bản đầu:** Những gì đề gốc yêu cầu và báo cáo cần có:
  - ViT.
  - CNN cùng số tham số.
  - Trực quan hóa attention.
  - Demo.
  - Phân tích lỗi và giới hạn.
- **Làm thêm nếu còn thời gian:** Grad-CAM, FLOPs, 3 seed, ViT pretrained, ablation, attention theo head và theo layer.
- **Ngoài phạm vi:** Deepfake (giáo viên đã xóa), train ở độ phân giải cao, API công khai, triển khai production.
- **Công nghệ, công cụ hoặc lựa chọn bắt buộc:** Đề bắt buộc ViT và dữ liệu Tiny ImageNet hoặc CIFAR-100. Nhóm tự chọn PyTorch và tự cài ViT.
- **Ràng buộc thời gian, chi phí, dữ liệu:** 13 ngày, chỉ có một máy GPU trong nhóm nên các lần train chạy lần lượt, không dùng test để chọn cấu hình, không bịa số liệu.
- **Lưu ý:** đây là diễn giải đề xuất; đối chiếu nghĩa Which với hướng dẫn của cô.

## How — Hướng thực hiện
- **Cách giải quyết tổng quát:** Chia train gốc 90/10 thành train và validation, dùng val gốc làm test. Train hai mô hình với cùng dữ liệu và số epoch, chọn checkpoint trên validation, đo trên test một lần.
- **AI hỗ trợ:** Claude Code hỗ trợ phân tích đề, soạn tài liệu và viết code; ghi nhận chi tiết trong [AI_Usage.md](../AI_Usage.md).
- **Người chịu trách nhiệm quyết định và kiểm tra:** Từng thành viên với phần của mình, TV1 duyệt cuối (phân công ở [04_BREAKDOWN.md](04_BREAKDOWN.md)).
- **Cách kiểm chứng dự kiến:** Test tự động, chạy thử `--quick`, đối chiếu số trong báo cáo với file kết quả; ghi vào [06_VERIFICATION.md](06_VERIFICATION.md).

## Input và output

| Luồng | Input | Output |
|---|---|---|
| Huấn luyện | Config YAML, dữ liệu đã chuẩn bị | Checkpoint, log CSV, đường cong học |
| Đánh giá | Checkpoint, tập test | Top-1, Top-5, per-class accuracy, top 20 cặp lớp nhầm, ảnh dự đoán sai |
| Trực quan hóa | Checkpoint ViT, ảnh test | Hình CLS attention và attention rollout |
| Demo | Một ảnh tải lên | Top-5 của ViT và CNN, ảnh attention rollout |

## Câu hỏi và giả định chưa chốt

| Nội dung | Tác động nếu sai | Ai xác nhận | Trạng thái |
|---|---|---|---|
| Nghĩa của "Which" trong mẫu Define | Phải sửa mục Which | TV1 hỏi giảng viên | Chưa xác nhận |
| Nhóm người dùng do nhóm tự đề xuất | Phải sửa mẫu đăng ký | Cả nhóm | Chưa xác nhận |
| Quyền sử dụng Tiny ImageNet cho mục đích học tập | Phải điền lại mẫu hoặc đổi dữ liệu | TV1 | Chưa xác nhận |
| Nơi nộp mẫu đăng ký, có cần duyệt không | Ảnh hưởng lịch | TV1 | Chưa xác nhận |
| Giảng viên có quy định khác ngoài phần đã thấy trên sheet | Thiếu sản phẩm phải nộp | TV1 | Chưa xác nhận |
| Tải được Tiny ImageNet từ Kaggle | Chuyển sang CIFAR-100 | TV4 | Chưa thử |
| Thành viên có GPU là ai | Chưa gán được TV4 | Cả nhóm | Chưa xác nhận |
| Batch 128 có vừa 6GB VRAM với cả ViT và CNN | Phải dùng batch 64 cho cả hai mô hình | TV4 | Chưa đo |
| Thời gian mỗi epoch trên máy GPU | Phải giảm epoch hoặc thí nghiệm | TV4 | Chưa đo |
