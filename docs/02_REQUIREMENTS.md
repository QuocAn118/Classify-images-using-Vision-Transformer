# Yêu cầu và tiêu chí nghiệm thu

Các ngưỡng số lấy từ [AGENT_SPEC_ViT_TinyImageNet.md](../AGENT_SPEC_ViT_TinyImageNet.md). Chưa yêu cầu nào được xác nhận hoàn thành; trạng thái ở [04_BREAKDOWN.md](04_BREAKDOWN.md).

## Yêu cầu chức năng

### FR-001: Chuẩn bị dữ liệu
- **Người sử dụng:** Thành viên nhóm, giảng viên chạy lại.
- **Mục đích:** Có dữ liệu đúng cấu trúc và không rò rỉ giữa các tập.
- **Điều kiện trước / đầu vào:** File Tiny ImageNet đã tải, đường dẫn trong `data.root`.
- **Luồng bình thường:** Giải nén, sắp xếp `val/` theo lớp, kiểm tra số lượng, xuất train/val/test thành mảng `uint8` (.npy) đã resize về `img_size`, in và lưu thống kê.
- **Quy tắc nghiệp vụ:** Train gốc chia 90/10 có phân tầng, seed cố định; val gốc là test; test gốc không nhãn bị bỏ qua.
- **Lỗi và biên:** Thiếu file hoặc sai số lượng thì dừng và báo rõ; chạy lại lần hai không làm hỏng dữ liệu.
- **Kết quả:** Mảng cache, `class_names.json`, `dataset_stats.json` (gồm thông tin cache), `samples.png`.

### FR-002: ViT tự cài
- **Người sử dụng:** TV4 (train), TV2 (attention), TV5 (demo).
- **Mục đích:** Có mô hình chính đúng đề và lấy được attention.
- **Điều kiện trước / đầu vào:** Tensor ảnh (B,3,H,W), cấu hình trong YAML.
- **Luồng bình thường:** Patch embedding, ghép CLS và positional embedding, qua các encoder block, lấy CLS rồi phân loại.
- **Quy tắc nghiệp vụ:** Không dùng mô hình dựng sẵn từ thư viện; kích thước lưới tính từ `img_size // patch_size`; khi train dùng `scaled_dot_product_attention`, khi `return_attn=True` dùng nhánh tính tường minh.
- **Lỗi và biên:** `img_size` không chia hết cho `patch_size` thì báo lỗi; attention lấy trước dropout.
- **Kết quả:** Logits, và danh sách attention khi `return_attn=True`.

### FR-003: CNN cùng số tham số
- **Người sử dụng:** TV4, TV5.
- **Mục đích:** Có baseline so sánh công bằng.
- **Điều kiện trước / đầu vào:** Số tham số mục tiêu của ViT.
- **Luồng bình thường:** `match_param_count` tìm cấu hình ResNet nhỏ và in kết quả.
- **Quy tắc nghiệp vụ:** Stem 3x3 stride 1 nhưng tầng đầu tiên downsample sớm, hoặc stem stride 2 (tránh feature map 64x64 ở nhiều tầng, vì tốn VRAM và thời gian); cấu hình cuối do `match_param_count` chọn; chênh lệch không quá 5%.
- **Lỗi và biên:** Không tìm được cấu hình đạt thì báo lỗi.
- **Kết quả:** Mô hình và số tham số thực tế.

### FR-004: Huấn luyện
- **Người sử dụng:** TV4.
- **Mục đích:** Train được từ một lệnh và chịu được ngắt phiên.
- **Điều kiện trước / đầu vào:** Config, dữ liệu đã chuẩn bị.
- **Luồng bình thường:** Mỗi epoch train, đánh giá validation, ghi log, lưu checkpoint tốt nhất và cuối.
- **Quy tắc nghiệp vụ:** Chọn checkpoint theo validation Top-1, không đọc test; AdamW cho kết quả so sánh chính; lr của CNN mặc định 2,5e-4, nếu chỉnh thì chỉ dựa trên validation; tên lần chạy gồm cả seed.
- **Lỗi và biên:** `--resume` tiếp tục không trùng dòng log; phiên bị ngắt lúc lưu không hỏng checkpoint cũ; không có GPU thì dùng CPU.
- **Kết quả:** Checkpoint, log CSV, hình đường cong học.

### FR-005: Đánh giá và phân tích lỗi
- **Người sử dụng:** TV5.
- **Mục đích:** Có số cuối và hiểu vì sao mô hình sai.
- **Điều kiện trước / đầu vào:** Checkpoint đã chốt, tập test.
- **Luồng bình thường:** Tính chỉ số, xuất per-class accuracy, cặp lớp nhầm và lưới ảnh sai.
- **Quy tắc nghiệp vụ:** Đánh giá test sau khi chốt cấu hình, cùng tập test cho hai mô hình. Ablation chỉ báo kết quả trên validation. Test chỉ dùng cho các mô hình chính cuối cùng (ViT và CNN).
- **Lỗi và biên:** Checkpoint không khớp mô hình thì báo lỗi.
- **Kết quả:** JSON kết quả, CSV per-class, hình lỗi.

### FR-006: Trực quan hóa attention
- **Người sử dụng:** TV2, người đọc báo cáo.
- **Mục đích:** Thấy ViT nhìn vào vùng nào.
- **Điều kiện trước / đầu vào:** Checkpoint ViT, ảnh test.
- **Luồng bình thường:** Lấy attention, tính CLS map và rollout, phủ heatmap lên ảnh.
- **Quy tắc nghiệp vụ:** Chọn cả ảnh dự đoán đúng và sai, nhiều lớp khác nhau.
- **Lỗi và biên:** Lưới phải đúng với mọi `patch_size` hợp lệ.
- **Kết quả:** Hình trong `outputs/figures/attention/`.

### FR-007: So sánh
- **Người sử dụng:** TV5, người đọc báo cáo.
- **Mục đích:** Có bảng so sánh ViT và CNN.
- **Điều kiện trước / đầu vào:** JSON kết quả của các mô hình.
- **Luồng bình thường:** Đọc JSON, sinh bảng và biểu đồ.
- **Quy tắc nghiệp vụ:** Mọi số lấy từ file; bảng bắt buộc có cột FLOPs/MACs (đo nếu làm được, ghi "chưa có" nếu chưa).
- **Lỗi và biên:** Số chưa có thì hiển thị "chưa có", không tự điền.
- **Kết quả:** `comparison.md`, `comparison.csv`, biểu đồ.

### FR-008: Demo
- **Người sử dụng:** Người xem demo, giảng viên.
- **Mục đích:** Thử mô hình trên một ảnh.
- **Điều kiện trước / đầu vào:** Checkpoint ViT và CNN (chứa tên lớp và mean/std, không cần bộ dữ liệu), ảnh tải lên.
- **Luồng bình thường:** Tải ảnh, tự resize, hiển thị Top-5 của hai mô hình và ảnh attention rollout.
- **Quy tắc nghiệp vụ:** Chạy được trên CPU; có ảnh mẫu trong `app/examples/`.
- **Lỗi và biên:** Thiếu checkpoint hoặc file không phải ảnh thì báo lỗi dễ hiểu; ảnh xám hoặc có kênh alpha được chuyển về RGB.
- **Kết quả:** Giao diện Gradio trả kết quả.

### FR-009: Tài liệu và báo cáo
- **Người sử dụng:** Giảng viên, cả nhóm.
- **Mục đích:** Đáp ứng yêu cầu báo cáo và quy trình `.agents/`.
- **Điều kiện trước / đầu vào:** Code, kết quả, nhật ký.
- **Luồng bình thường:** Cập nhật `docs/`, `README.md`, `AI_Usage.md`, `report/report.md`.
- **Quy tắc nghiệp vụ:** Báo cáo gồm vấn đề và phạm vi, dữ liệu mẫu và mô tả, mã nguồn, hướng dẫn cài đặt/chạy, demo, kết quả so với baseline, phân tích lỗi và giới hạn.
- **Lỗi và biên:** Chưa có số thì ghi "chưa có"; không ghi lệnh chưa chạy thành công như đã chạy.
- **Kết quả:** Bộ tài liệu khớp code.

## Tiêu chí nghiệm thu

| Mã | Điều kiện ban đầu | Thao tác | Kết quả mong đợi |
|---|---|---|---|
| AC-001 | Có file Tiny ImageNet | Chạy `scripts/prepare_data.py` | Báo 200 lớp, 100.000 ảnh train gốc, 10.000 ảnh val gốc |
| AC-002 | Dữ liệu đã chuẩn bị | Tạo các tập | 90.000 train, 10.000 validation, 10.000 test; train và validation không trùng ảnh; mỗi lớp 450/50; có mảng cache khoảng 1,35 GB (tính tay); chạy lại không làm hỏng |
| AC-003 | Thiếu thư mục dữ liệu | Chạy `scripts/prepare_data.py` | Dừng, báo lỗi kèm hướng dẫn tải |
| AC-004 | ViT cấu hình mặc định | Forward input (2,3,64,64) | Output (2,200) |
| AC-005 | ViT ở `eval()` | Gọi `return_attn=True` | Mỗi layer có attention (B,heads,N+1,N+1), mỗi hàng tổng bằng 1 (sai số 1e-4); logits hai nhánh chênh tuyệt đối tối đa 1e-4 |
| AC-006 | ViT và CNN mặc định | Đếm tham số | Chênh không quá 5% |
| AC-007 | Không có dữ liệu thật, CPU | Chạy train với `--quick` | Dùng dữ liệu giả và in cảnh báo; kết thúc không lỗi, có checkpoint và log CSV |
| AC-008 | Train bị ngắt sau epoch k | Chạy `--resume` | Tiếp tục từ epoch k+1, log không trùng dòng, lr schedule khớp với chạy liền mạch (chênh không quá 1e-8), `val_loss` ở epoch k+1 chênh không quá 10% so với epoch k (không đòi trọng số giống hệt, vì shuffle, augmentation và GPU không tất định) |
| AC-009 | Có checkpoint | Chạy `src.evaluate` | Có Top-1, Top-5, per-class CSV, top 20 cặp nhầm, hình ảnh sai cho cả hai mô hình |
| AC-010 | Có checkpoint ViT | Chạy `src.attention` | Có hình cho ít nhất 12 ảnh, gồm cả đúng và sai |
| AC-011 | Có JSON kết quả | Chạy `src.compare` | Bảng khớp với JSON; số thiếu hiện "chưa có" |
| AC-012 | Có checkpoint, CPU | Chạy `app/demo.py`, tải ảnh lên | Hiển thị Top-5 hai mô hình và ảnh attention |
| AC-013 | Config thiếu khóa bắt buộc | Nạp config | Báo lỗi nêu tên khóa thiếu |
| AC-014 | Có bản báo cáo cuối | Đối chiếu từng số với file kết quả | Tất cả khớp, đủ 7 mục đề yêu cầu |

## Yêu cầu chất lượng phù hợp dự án
- **Phân quyền, bảo vệ dữ liệu:** Không commit `kaggle.json`, dữ liệu hoặc checkpoint. Nạp checkpoint với `weights_only=True`.
- **Hiệu năng:** Máy train có 6GB VRAM. Mặc định batch 64, lr ViT 2,5e-4, ViT và CNN cùng batch. Đo VRAM đỉnh bằng `--quick` trước khi train thật. Chưa đặt ngưỡng tốc độ; đo và báo cáo thời gian mỗi epoch và số ảnh/giây.
- **Độ tin cậy kết quả:** Tập test 10.000 ảnh cho sai số khoảng ±0,5 điểm phần trăm, và chỉ có 1 seed. Chênh lệch giữa ViT và CNN dưới khoảng 1–1,5 điểm không đủ để kết luận mô hình nào tốt hơn. Nếu chạy 3 seed thì cập nhật câu này.
- **Khả năng tái lập:** Seed cố định, siêu tham số nằm trong YAML, không hardcode đường dẫn.
- **Khả năng bảo trì:** Type hint, docstring ngắn. Từ TASK-001 trở đi, thay đổi đi qua nhánh riêng và PR có người review (TV1 duyệt; PR của chính TV1 do TV4 duyệt); giai đoạn tài liệu làm thẳng trên `main`.
- **Thiết bị và trình duyệt hỗ trợ:** Python 3.10+; demo chạy trên trình duyệt bằng CPU.

## Theo dõi liên kết

| Yêu cầu | Thiết kế liên quan | Đầu việc | Kiểm chứng |
|---|---|---|---|
| FR-001 / AC-001, 002, 003 | Luồng dữ liệu | TASK-002, TASK-003 | Chưa có |
| FR-002 / AC-004, 005 | Mô hình, interface mô hình | TASK-004 | Chưa có |
| FR-003 / AC-006 | Mô hình | TASK-005 | Chưa có |
| FR-004 / AC-007, 008 | Interface checkpoint, log | TASK-001, TASK-006, TASK-011 | Chưa có |
| FR-005 / AC-009 | Interface kết quả | TASK-007, TASK-012 | Chưa có |
| FR-006 / AC-010 | Interface mô hình | TASK-008 | Chưa có |
| FR-007 / AC-011 | Interface kết quả | TASK-009 | Chưa có |
| FR-008 / AC-012 | Luồng demo | TASK-010 | Chưa có |
| FR-009 / AC-014 | Toàn bộ | TASK-012, TASK-014 | Chưa có |
| AC-013 | Interface config | TASK-001 | Chưa có |
