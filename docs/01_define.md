# Define: bài toán và phạm vi

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
- **Mức Top-1 dự đoán (không phải chỉ số thành công):** ViT khoảng 40%, CNN khoảng 50%; không phải cam kết và không phải điều kiện đạt, có thể thấp hơn khi chỉ train 50 epoch.

## When — Khi nào?
- **Tình huống/kích hoạt:** Người dùng chạy lệnh train, đánh giá hoặc mở demo khi cần kết quả; giảng viên chạy lại theo README khi chấm.
- **Thời hạn và mốc:** Hạn nộp 2026-11-25 (giảng viên gia hạn từ 2026-11-20), nhóm đặt mục tiêu nộp 2026-11-24. Các mốc ở [03_plan.md](03_plan.md).

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
- **Ngoài phạm vi:** ViT pretrained (nhóm quyết định bỏ), train ở độ phân giải cao, API công khai, triển khai production.
- **Công nghệ, công cụ hoặc lựa chọn bắt buộc:** Đề bắt buộc ViT và dữ liệu Tiny ImageNet hoặc CIFAR-100. Nhóm tự chọn PyTorch và tự cài ViT.
- **Ràng buộc thời gian, chi phí, dữ liệu:** Khoảng 10 ngày tính từ 15/11, chỉ có một máy GPU trong nhóm nên các lần train chạy lần lượt, không dùng test để chọn cấu hình, không bịa số liệu.
- **Lưu ý:** đây là diễn giải đề xuất; đối chiếu nghĩa Which với hướng dẫn của cô.

## How — Hướng thực hiện
- **Cách giải quyết tổng quát:** Chia train gốc 90/10 thành train và validation, dùng val gốc làm test. Train hai mô hình với cùng dữ liệu và số epoch, chọn checkpoint trên validation, đo trên test một lần.
- **AI hỗ trợ:** Claude Code hỗ trợ phân tích đề, soạn tài liệu và viết code; ghi nhận chi tiết trong [AI_Usage.md](../AI_Usage.md).
- **Người chịu trách nhiệm quyết định và kiểm tra:** Từng thành viên với phần của mình, TV1 duyệt cuối (phân công ở [03_plan.md](03_plan.md)).
- **Cách kiểm chứng dự kiến:** Test tự động, chạy thử `--quick`, đối chiếu số trong báo cáo với file kết quả. Bằng chứng ghi trong PR của từng đầu việc.

## Input và output

| Luồng | Input | Output |
|---|---|---|
| Huấn luyện | Config YAML, dữ liệu đã chuẩn bị | Checkpoint, log CSV, đường cong học |
| Đánh giá | Checkpoint, tập test | Top-1, Top-5, per-class accuracy, top 20 cặp lớp nhầm, ảnh dự đoán sai |
| Trực quan hóa | Checkpoint ViT, ảnh test | Hình CLS attention và attention rollout |
| Demo | Một ảnh tải lên | Top-5 của ViT và CNN, ảnh attention rollout |

## Yêu cầu chức năng

Chi tiết từng yêu cầu và tiêu chí nghiệm thu (AC) nằm ở file thành phần. Các ngưỡng số lấy từ [SPEC_ViT.md](../SPEC_ViT.md).

| Mã | Yêu cầu | AC | File |
|---|---|---|---|
| FR-001 | Chuẩn bị dữ liệu | AC-001, 002, 003 | [04_data.md](04_data.md) |
| FR-002 | ViT tự cài | AC-004, 005 | [05_model.md](05_model.md) |
| FR-003 | CNN cùng số tham số | AC-006 | [05_model.md](05_model.md) |
| FR-004 | Huấn luyện | AC-007, 008 | [06_training.md](06_training.md) |
| FR-005 | Đánh giá và phân tích lỗi | AC-009 | [07_evaluation.md](07_evaluation.md) |
| FR-006 | Trực quan hóa attention | AC-010 | [07_evaluation.md](07_evaluation.md) |
| FR-007 | So sánh | AC-011 | [07_evaluation.md](07_evaluation.md) |
| FR-008 | Demo | AC-012 | [08_demo.md](08_demo.md) |
| FR-009 | Tài liệu và báo cáo | AC-014 | Mục dưới |
| | Config dùng chung | AC-013 | [02_architecture.md](02_architecture.md) |

### FR-009: Tài liệu và báo cáo
- **Người sử dụng:** Giảng viên, cả nhóm.
- **Mục đích:** Đáp ứng yêu cầu báo cáo và quy trình `workflow/`.
- **Luồng bình thường:** Cập nhật `docs/`, `README.md`, `AI_Usage.md`, `report/report.md`.
- **Quy tắc:** Báo cáo gồm vấn đề và phạm vi, dữ liệu mẫu và mô tả, mã nguồn, hướng dẫn cài đặt/chạy, demo, kết quả so với baseline, phân tích lỗi và giới hạn.
- **Lỗi và biên:** Chưa có số thì ghi "chưa có"; không ghi lệnh chưa chạy thành công như đã chạy.

| Mã | Điều kiện ban đầu | Thao tác | Kết quả mong đợi |
|---|---|---|---|
| AC-014 | Có bản báo cáo cuối | Đối chiếu từng số với file kết quả | Tất cả khớp, đủ 7 mục đề yêu cầu |

## Yêu cầu chất lượng
- **Phân quyền, bảo vệ dữ liệu:** Không commit `kaggle.json`, dữ liệu hoặc checkpoint. Nạp checkpoint với `weights_only=True`.
- **Hiệu năng:** Máy train có 6GB VRAM. Mặc định batch 64, lr 2,5e-4, ViT và CNN cùng batch. Đo VRAM đỉnh bằng `--quick` trước khi train thật. Chưa đặt ngưỡng tốc độ; đo và báo cáo thời gian mỗi epoch và số ảnh/giây.
- **Độ tin cậy kết quả:** Tập test 10.000 ảnh cho sai số khoảng ±0,5 điểm phần trăm, và chỉ có 1 seed. Chênh lệch giữa ViT và CNN dưới khoảng 1–1,5 điểm không đủ để kết luận mô hình nào tốt hơn. Nếu chạy 3 seed thì cập nhật câu này.
- **Khả năng tái lập:** Seed cố định, siêu tham số nằm trong YAML, không hardcode đường dẫn.
- **Khả năng bảo trì:** Type hint, docstring ngắn. Thay đổi của TV2-TV5 đi qua nhánh riêng và PR có TV1 review; TV1 làm thẳng trên `main`, nên phần của TV1 được kiểm bằng test tự động thay cho review.
- **Thiết bị và trình duyệt hỗ trợ:** Python 3.10+; demo chạy trên trình duyệt bằng CPU.

## Câu hỏi và giả định chưa chốt

| Nội dung | Tác động nếu sai | Ai xác nhận | Trạng thái |
|---|---|---|---|
| Nghĩa của "Which" trong mẫu Define | Phải sửa mục Which | TV1 hỏi giảng viên | Chưa xác nhận |
| Nhóm người dùng do nhóm tự đề xuất | Phải sửa mẫu đăng ký | Cả nhóm | Chưa xác nhận |
| Quyền sử dụng Tiny ImageNet cho mục đích học tập | Phải điền lại mẫu hoặc đổi dữ liệu | TV1 | Chưa xác nhận |
| Nơi nộp mẫu đăng ký, có cần duyệt không | Ảnh hưởng lịch | TV1 | Đã nộp 15/11; giảng viên chưa phản hồi về việc duyệt |
| Giảng viên có quy định khác ngoài phần đã thấy trên sheet | Thiếu sản phẩm phải nộp | TV1 | Chưa xác nhận |
| Bằng chứng các bước Describe, Review, Test, Commit để trên GitHub Issue/PR thay vì file trong `docs/` | Phải chép lại vào file | TV1 hỏi giảng viên | Chưa xác nhận |
| Tải được Tiny ImageNet từ Kaggle | Chuyển sang CIFAR-100 | TV1 (TASK-002) | 2026-11-16: trang cuộc thi Kaggle báo "Invitation required", không tải được; tải từ Stanford thay thế (DEC-015) |
| Thành viên có GPU là ai | Chưa gán được TV4 | Cả nhóm | Chưa xác nhận |
| Batch 64 có vừa 6GB VRAM với cả hai mô hình (đặc biệt CNN) | Dùng gradient accumulation hoặc giảm batch còn 32 với cả hai mô hình | TV4 | Chưa đo |
| Thời gian mỗi epoch trên máy GPU. Dự đoán, ước tính thô, chưa đo: ViT khoảng 1–2 phút/epoch, CNN khoảng 3–6 phút/epoch trên GPU 6GB cỡ phổ thông, nên 50 epoch cho cả hai khoảng 4–6 giờ. Số của CNN tính cho stem cũ chưa downsample, thiết kế mới có thể nhanh hơn. Phải đo thật trước khi chốt số thí nghiệm. | Phải cắt thí nghiệm hoặc chuyển phần còn lại sang Kaggle/Colab (50 epoch là mức sàn) | TV4 | Chưa đo |
