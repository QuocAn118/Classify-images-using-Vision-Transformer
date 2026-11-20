# Báo cáo: Phân loại ảnh Tiny ImageNet bằng Vision Transformer

> **Bản nháp, phần TV2 cập nhật ngày 2026-11-20.** Khung theo mục 15 của [spec](../SPEC_ViT.md). Đã có mục 2 (dữ liệu), 3.1 và 4.1 (ViT), 3.2 (CNN), mục 6 (attention trên checkpoint thật). Tổng hợp huấn luyện, đánh giá accuracy và các phần còn thiếu chờ thành viên phụ trách bổ sung; phần TASK-008 chờ TV1 review.

**Phân công viết** (theo mục 19 spec; TV5 ghép bản cuối):

| Mục | Người viết | Viết khi có |
|---|---|---|
| 1, 2, 8, 9 | TV1 | 2 đã có; 1 viết ngay; 8, 9 sau khi có train, đánh giá, demo |
| 3.1, 6 | TV2 | Đã có kiến trúc và hình attention thật; TASK-008 chờ TV1 review |
| 3.2, 6.4 (Grad-CAM, nếu làm) | TV3 | Sau TASK-005 |
| 3.3, 4 | TV4 | Sau TASK-006, TASK-011 |
| 5, 7, 10 | TV5 | Sau TASK-007, TASK-009 |

**Quy tắc chung khi viết:**
- Mọi con số phải dẫn về file trong `outputs/results/` hoặc `outputs/logs/`; chưa có thì ghi "chưa có" (mục 17 spec).
- Không dùng tập test để chọn cấu hình hay checkpoint; số trên test chỉ chạy một lần sau khi chốt.
- Hình để trong `outputs/figures/`, chèn bằng đường dẫn tương đối.
- Mỗi mục bắt đầu bằng danh sách "Cần có" bên dưới; viết xong thì xóa danh sách đó.

## 1. Vấn đề và phạm vi

*Người viết: TV1.* Chưa viết.

Cần có: bài toán; vì sao chọn ViT và so sánh với CNN cùng số tham số; phạm vi bắt buộc (ViT tự cài, baseline CNN, attention) và phần mở rộng. Nguồn: [docs/01_define.md](../docs/01_define.md).

## 2. Dữ liệu

*Người viết: TV1.*

**Nguồn.** Tiny ImageNet của Stanford CS231n, tải từ `https://cs231n.stanford.edu/tiny-imagenet-200.zip` (248 MB). Repo không chứa dữ liệu; `python scripts/prepare_data.py --download` tải và chuẩn bị lại trên mọi máy (DEC-015).

**Quy mô.** 200 lớp, ảnh RGB 64 × 64. Bộ gốc có 100.000 ảnh train (500 ảnh/lớp), 10.000 ảnh val có nhãn và 10.000 ảnh test không có nhãn.

**Chia tập.** Tập test gốc không có nhãn nên bị bỏ. Để có tập chọn cấu hình riêng và tập đánh giá cuối không bị dùng trong lúc phát triển, nhóm chia như sau:

| Tập | Lấy từ | Số ảnh | Mỗi lớp | Dùng để |
|---|---|---|---|---|
| Train | 90% train gốc, chia phân tầng, seed 42 | 90.000 | 450 | Huấn luyện, có augmentation |
| Validation | 10% còn lại của train gốc | 10.000 | 50 | Chọn siêu tham số và checkpoint |
| Test | Val gốc | 10.000 | 50 | Đánh giá cuối, chạy một lần |

Train và validation lấy từ hai tập chỉ số không giao nhau. Số lượng đọc từ [dataset_stats.json](../outputs/results/dataset_stats.json) và đã đếm lại trên mảng nhãn của cache ngày 2026-11-16.

**Tiền xử lý.** Ảnh được giải mã một lần và lưu thành mảng `uint8` (tổng 1,35 GB) để DataLoader không phải đọc 110.000 file JPEG mỗi epoch. Chuẩn hóa bằng mean/std của ImageNet. Augmentation khi train: RandomCrop 64 với padding 4, lật ngang, RandAugment; validation và test chỉ chuẩn hóa. Mixup/CutMix áp ở vòng lặp train (mục 3.3).

![25 ảnh train ngẫu nhiên kèm tên lớp](../outputs/figures/samples.png)

*Hình 1. 25 ảnh ngẫu nhiên từ tập train (seed 42). Tên lớp lấy từ [class_names.json](../outputs/results/class_names.json).*

## 3. Phương pháp

### 3.1. Kiến trúc ViT (TV2)

Vision Transformer biểu diễn ảnh thành một chuỗi patch và dùng Transformer để xử lý quan hệ giữa các patch. Ý tưởng chia ảnh thành token và sử dụng token phân loại được tham khảo từ [Dosovitskiy và cộng sự](https://arxiv.org/abs/2010.11929). Trong đồ án, nhóm tự cài mô hình bằng PyTorch, không sử dụng ViT dựng sẵn hoặc trọng số pretrained.

Biến thể dùng trong repo có tên cấu hình `vit_small`. Các kích thước và siêu tham số dưới đây được lấy từ [vit_small.yaml](../configs/vit_small.yaml); đây là cấu hình riêng của đồ án.

| Thuộc tính | Giá trị |
|---|---|
| Ảnh đầu vào | RGB, 64 × 64 |
| Patch | 8 × 8, không chồng lấn |
| Số patch / tổng số token có CLS | 64 / 65 |
| Chiều embedding | 256 |
| Số encoder block | 8 |
| Số attention head mỗi block | 8 |
| MLP ratio | 4 |
| Dropout | 0,0 |
| DropPath lớn nhất | 0,1 |
| Số lớp đầu ra | 200 |
| Số tham số đã đếm bằng code | 6.436.296 |

Số tham số và shape forward mặc định đã được kiểm tra, lưu tại [task004_vit_checks.json](../outputs/results/task004_vit_checks.json). Mã nguồn mô hình nằm trong [vit.py](../src/models/vit.py).

```mermaid
flowchart TD
    I["Ảnh: B × 3 × 64 × 64"] --> P["PatchEmbedding: Conv2d kernel 8, stride 8"]
    P --> T["Chuỗi patch: B × 64 × 256"]
    T --> C["Ghép CLS, cộng positional embedding: B × 65 × 256"]
    C --> E["8 encoder Pre-LN: attention + MLP, residual và DropPath"]
    E --> N["LayerNorm cuối, lấy token CLS: B × 256"]
    N --> H["Linear 256 → 200"]
    H --> O["Logits: B × 200"]
```

**Patch embedding và vị trí.** Với ảnh vuông cạnh $H$ và patch cạnh $P$, số patch là $N=(H/P)^2$. `PatchEmbedding` dùng Conv2d có kernel và stride bằng $P$, sau đó trải phẳng hai chiều không gian thành chuỗi. Một CLS token học được được ghép ở đầu chuỗi để tổng hợp thông tin phục vụ phân loại. Positional embedding học được có shape `(1,N+1,D)` được cộng vào chuỗi để biểu diễn vị trí của từng token. Trong cấu hình mặc định, chuỗi sau bước này có shape `(B,65,256)`.

**Encoder Pre-LN.** Mỗi block áp LayerNorm trước attention và trước MLP, với hai kết nối residual:

$$
U_l = Z_{l-1} + \operatorname{DropPath}_l\bigl(\operatorname{MSA}(\operatorname{LN}_1(Z_{l-1}))\bigr),
$$

$$
Z_l = U_l + \operatorname{DropPath}_l\bigl(\operatorname{MLP}(\operatorname{LN}_2(U_l))\bigr).
$$

MSA là multi-head self-attention. MLP gồm Linear mở rộng chiều embedding theo `mlp_ratio`, GELU, dropout, Linear đưa về chiều ban đầu và dropout. `DropPath` bỏ toàn bộ nhánh residual theo từng ảnh khi train, đồng thời chia cho xác suất giữ nhánh để bảo toàn kỳ vọng. Xác suất bỏ nhánh tăng tuyến tính theo độ sâu, từ 0 đến 0,1 ở cấu hình mặc định. Khi `eval()`, DropPath và dropout đều tắt.

**Hai nhánh attention.** Từ embedding của mỗi token, một Linear chung tạo $Q$, $K$, $V$, rồi chia thành các head. Với chiều mỗi head là $d_h$:

$$
A = \operatorname{softmax}\left(\frac{QK^T}{\sqrt{d_h}}\right),
\qquad O = \operatorname{Dropout}(A)V.
$$

Nhánh forward thường dùng `torch.nn.functional.scaled_dot_product_attention` để tính attention; khi eval, xác suất dropout được truyền tường minh là 0. Nhánh `return_attn=True` tính công thức trên trực tiếp, dùng chung trọng số qkv/proj và trả thêm $A$ **trước dropout**. Mỗi layer trả một tensor `(B,heads,N+1,N+1)`. Nhánh này cung cấp đầu vào cho phần trực quan hóa; bản thân việc trả weights chưa tạo ra hình attention hoặc chứng minh chất lượng dự đoán.

**Head và khởi tạo.** Sau encoder cuối, LayerNorm được áp lên chuỗi, lấy biểu diễn CLS và đưa qua Linear để tạo logits. Mô hình không softmax logits, để bên huấn luyện có thể dùng CrossEntropyLoss. Trọng số Linear, CLS token và positional embedding được khởi tạo bằng truncated normal với độ lệch chuẩn 0,02; bias Linear bằng 0, LayerNorm có weight bằng 1 và bias bằng 0. Đây là các giá trị khởi tạo trong code, không phải kết quả huấn luyện.

**Tích hợp.** Các thành phần khác tạo mô hình qua `build_model(cfg)` trong [src/models/__init__.py](../src/models/__init__.py). Hàm lấy `img_size`, `num_classes` từ phần `data` và các thuộc tính kiến trúc từ phần `model`, không sửa config của bên gọi. Mô hình báo lỗi nếu kích thước ảnh không chia hết cho patch, chiều embedding không chia hết cho số head hoặc input không đúng shape RGB đã cấu hình. Hợp đồng chi tiết được giữ tại [docs/05_model.md](../docs/05_model.md).

### 3.2. Baseline CNN và khớp số tham số (TV3)

Để so sánh với Vision Transformer, nhóm xây dựng một baseline CNN dựa trên kiến trúc ResNet nhỏ (`ResNetSmall`), sử dụng BasicBlock và BatchNorm. Mô hình được cài đặt bằng PyTorch, không sử dụng kiến trúc dựng sẵn hoặc trọng số pretrained.

**Cấu hình kiến trúc.** Các tham số kiến trúc được khai báo trong `configs/cnn_baseline.yaml`:

| Thuộc tính | Giá trị |
|---|---|
| Kiến trúc | ResNet-small |
| Block | BasicBlock |
| Normalization | BatchNorm |
| Số kênh các stage (`widths`) | [64, 128, 256, 512] |
| Số block mỗi stage (`blocks`) | [1, 2, 2, 1] |
| Stride của stem | 2 |
| Ảnh đầu vào | RGB, 64 × 64 |
| Số lớp đầu ra | 200 |

Cấu hình được truyền vào `ResNetSmall` thông qua `build_model(cfg)`. Các thông số kiến trúc được đọc từ file YAML thay vì hard-code trong hàm khởi tạo mô hình. Việc tạo mô hình không thực hiện tìm kiếm cấu hình khớp số tham số, tránh phát sinh chi phí tính toán không cần thiết ở mỗi lần khởi tạo.

**Khớp số tham số.** Nhóm sử dụng hàm `match_param_count()` trong `src/models/cnn.py` để tìm cấu hình ResNet có số tham số gần với mô hình ViT. Mục tiêu được lấy từ số tham số thực tế của ViT-small là 6.436.296. Cấu hình được chọn phải có sai lệch tương đối không quá 5% so với mục tiêu. Hàm cũng báo `ValueError` khi không tìm được cấu hình đáp ứng yêu cầu.

Sau khi xây dựng mô hình bằng cấu hình đã chọn, số tham số được đếm trực tiếp từ các tham số của mô hình:

| Mô hình | Số tham số | Sai lệch tương đối so với ViT |
|---|---:|---:|
| ViT-small | 6.436.296 | — |
| ResNet-small | 6.476.808 | 0,63% |

Sai lệch 0,63% thấp hơn giới hạn 5%, đáp ứng yêu cầu so sánh hai mô hình có quy mô tham số tương đương.

**Chi phí tính toán.** FLOPs được đo bằng `torch.utils.flop_counter.FlopCounterMode`, với cả hai mô hình ở chế độ `eval()` và đầu vào có shape `(1, 3, 64, 64)`. Kết quả được tính theo FLOPs trên một ảnh:

| Mô hình | FLOPs / ảnh |
|---|---:|
| ViT-small | 824.283.136 |
| ResNet-small | 809.050.112 |

ResNet-small có số FLOPs thấp hơn ViT-small 15.233.024 FLOPs/ảnh, tương đương khoảng 1,85%. Đây là kết quả đo theo cùng công cụ và shape đầu vào. MACs chưa được đo riêng nên không suy diễn hoặc quy đổi từ FLOPs.

**Kiểm chứng cài đặt.** Các kiểm tra được bổ sung trong `tests/test_models.py`, gồm: so sánh số tham số CNN với ViT và xác nhận sai lệch không quá 5%; kiểm tra đầu ra CNN có shape `(2, 200)`; kiểm tra `match_param_count(6_436_296)` tìm được cấu hình hợp lệ; và xác nhận hàm báo `ValueError` với mục tiêu quá nhỏ. Riêng nhóm test mô hình đạt 27 test. Sau khi tích hợp, toàn bộ test suite của repo chạy bằng `python -m pytest -q -W error` đạt **52 passed**.

Các số liệu và kết quả kiểm tra TASK-005 được lưu tại [task005_cnn_checks.json](../outputs/results/task005_cnn_checks.json). Mã nguồn kiến trúc nằm trong [cnn.py](../src/models/cnn.py), cấu hình tại [cnn_baseline.yaml](../configs/cnn_baseline.yaml).

Kết quả trên xác nhận baseline CNN đáp ứng yêu cầu về số tham số tương đương và đã vượt qua các kiểm tra chức năng. Đây là kiểm chứng cài đặt và đo chi phí tính toán, chưa phải kết quả đánh giá độ chính xác sau huấn luyện trên Tiny ImageNet.

### 3.3. Công thức huấn luyện và augmentation

*Người viết: TV4.* Chưa có.

Cần có: optimizer, lịch learning rate (warmup, cosine), batch size, số epoch, label smoothing, Mixup/CutMix, AMP, gradient clipping, cách chọn checkpoint trên validation. Lấy giá trị từ `configs/*.yaml` thật đã chạy, không chép từ spec. Nguồn: [docs/06_training.md](../docs/06_training.md).

## 4. Thực nghiệm

### 4.1. Kiểm chứng cài đặt ViT đã thực hiện

Đây là kiểm chứng chức năng mô hình bằng dữ liệu giả, không phải thí nghiệm đo accuracy trên Tiny ImageNet. Kết quả sau lấy từ [task004_vit_checks.json](../outputs/results/task004_vit_checks.json), chạy ngày 2026-11-17 trên CPU với Python 3.12.10 và torch 2.15.0+cpu, seed 42.

| Kiểm tra | Kết quả đã lưu |
|---|---|
| Input / logits | `(2,3,64,64)` → `(2,200)` |
| Attention | 8 layer, mỗi tensor `(2,8,65,65)` |
| Số tham số | 6.436.296 |
| Sai khác logits lớn nhất giữa hai nhánh ở eval | Khoảng 7,15 × 10⁻⁷, dưới ngưỡng 10⁻⁴ |
| Sai số lớn nhất của tổng hàng attention so với 1 | Khoảng 2,38 × 10⁻⁷, dưới ngưỡng 10⁻⁴ |
| Backward | Gradient của mọi tham số hữu hạn |
| Một bước AdamW trên batch giả | Trọng số head thay đổi |

Theo bằng chứng trong [nhật ký TASK-004](../docs/10_work_log.md), lệnh `python -m pytest tests/test_models.py -q -W error` đạt **23 test mô hình**, và `python -m pytest -q -W error` đạt **48 test toàn repo**. Bộ [test_models.py](../tests/test_models.py) bao phủ shape mặc định, attention, cấu hình lưới patch khác, input/config lỗi, train/eval của dropout và DropPath, backward qua cả hai nhánh và nạp state dict bằng `weights_only=True`. Các kiểm tra này đã chạy trong buổi triển khai; buổi viết báo cáo không chạy lại unit test vì code không đổi.

Những bằng chứng trên xác nhận mô hình có thể forward, truyền gradient và cập nhật tham số trong các trường hợp đã thử. Chúng chưa chứng minh mô hình học tốt hoặc đáp ứng giới hạn VRAM của máy train.

### 4.2. Huấn luyện, đường cong học và ablation

*Người viết: TV4.* Chưa có.

Cần có: máy và GPU đã dùng; kết quả chính trên validation; đường cong loss và accuracy theo epoch (hình từ `outputs/logs/`); ablation nếu có. Bắt buộc ghi câu: ngân sách 50 epoch có thể làm ViT thiệt hơn CNN, nên kết luận ViT so với CNN chỉ đúng trong ngân sách này. Top-1, Top-5, thời gian mỗi epoch, tốc độ inference và VRAM đỉnh hiện **chưa có**; không dùng kết quả trên batch giả để điền các chỉ số này.

## 5. So sánh ViT với CNN

*Người viết: TV5.* Chưa có.

Cần có: bảng so sánh theo mục 12 spec (Top-1, Top-5 trên test, số tham số, FLOPs/MACs, thời gian train, tốc độ inference, VRAM đỉnh), dẫn về file kết quả thực tế; nhận xét ViT thiếu inductive bias nên cần nhiều dữ liệu và augmentation; nêu rõ cùng số tham số không đồng nghĩa cùng chi phí tính toán. Chưa có cơ sở kết luận ViT tốt hơn hoặc kém hơn CNN; FLOPs/MACs chưa đo thì ghi "chưa có".

## 6. Trực quan hóa attention (TV2)

### 6.1. Mô hình và checkpoint dùng để trực quan hóa

ViT hỗ trợ `return_attn=True` để trả attention theo từng head và layer, trước dropout. Ở cấu hình mặc định, danh sách có 8 tensor `(B,8,65,65)`, trong đó token đầu tiên là CLS. Shape, tổng hàng và độ khớp logits giữa hai nhánh đã được kiểm tra như mục 4.1.

Ngày 2026-11-20, TV2 dùng checkpoint `vit_small_seed42_best.pt` do TV4 bàn giao, epoch 50, để sinh hình trên CPU. SHA-256 bắt đầu bằng `97fbd0daa0e0` khớp file best trong bằng chứng TASK-011 trên nhánh `hoangdang`; hash đầy đủ và thông tin kiểm chứng được lưu tại [task008_attention_checks.json](../outputs/results/task008_attention_checks.json). Kiến trúc, trọng số, tên lớp và mean/std đều lấy từ checkpoint; không train lại hoặc chọn checkpoint dựa trên test. Việc bàn giao checkpoint độc lập với việc review code train của TV4, vốn chưa gộp vào nhánh nền của TASK-008.

### 6.2. CLS attention map và attention rollout

Các phép biến đổi dưới đây đã được cài trong [src/attention.py](../src/attention.py), theo [docs/07_evaluation.md](../docs/07_evaluation.md) và spec. Hai loại map được nội suy bilinear và min-max riêng từng ảnh về `[0,1]`; map hằng cho toàn 0 để tránh chia cho 0. Heatmap dùng colormap jet, phủ lên ảnh RGB với alpha 0,5. Màu biểu diễn độ lớn tương đối trong từng map, không phải xác suất dự đoán và không dùng để so cường độ attention tuyệt đối giữa các ảnh.

**CLS attention map:** lấy hàng CLS tới các patch ở layer cuối, bỏ cột CLS, trung bình theo head rồi reshape thành lưới `img_size // patch_size`. Sau đó nội suy bilinear lên kích thước ảnh và phủ heatmap lên ảnh gốc. Với cấu hình mặc định, lưới patch là 8 × 8.

**Attention rollout:** kết hợp attention qua các layer theo phương pháp của [Abnar và Zuidema (2020)](https://aclanthology.org/2020.acl-main.385/). Với $A_l$ là attention trung bình theo head của layer $l$, phương án của đồ án bổ sung residual và chuẩn hóa theo hàng:

$$
\widetilde A_l = \operatorname{RowNorm}(0.5 A_l + 0.5 I),
\qquad R_0 = I,\quad R_l = \widetilde A_l R_{l-1}.
$$

Hàng CLS của $R_L$, bỏ cột CLS, được đưa về lưới patch để tạo heatmap. Bộ kiểm thử bao gồm ma trận tính tay kiểm thứ tự tích từ layer thấp đến cao, trung bình head, lưới patch khác, map hằng, overlay, checkpoint và pipeline sinh hình. Kết quả toàn repo là **73 test pass**, gồm **21 ca attention**, theo [file bằng chứng TASK-008](../outputs/results/task008_attention_checks.json).

### 6.3. Hình và nhận xét thực tế

**Chọn ảnh.** Dùng test của đồ án, tức val gốc Tiny ImageNet. Với seed 42 và checkpoint cố định, chương trình duyệt 512 ảnh theo thứ tự ngẫu nhiên đã xác định, chọn 12 ảnh gồm 6 đúng và 6 sai, ưu tiên nhãn thật chưa chọn. Kết quả có 12 lớp khác nhau. Các chỉ số ảnh, nhãn, dự đoán, confidence và đường dẫn hình nằm trong [manifest](../outputs/figures/attention/vit_small_seed42_test/manifest.json). Số lượng đúng/sai được cân bằng chủ động để minh họa; tập này không dùng để ước lượng Top-1/Top-5 hoặc chọn mô hình.

![Hình attention của 12 ảnh: gốc, CLS layer cuối và rollout](../outputs/figures/attention/vit_small_seed42_test/gallery.png)

*Mỗi hàng: ảnh gốc và nhãn/dự đoán, CLS attention layer cuối, attention rollout. Mỗi map được chuẩn hóa riêng; ảnh nền có độ phân giải 64 × 64, lưới patch 8 × 8. Tensor map được lưu trong `maps.npz` cùng thư mục để đối chiếu với hình.*

Một số ví dụ trong gallery (confidence là softmax của lớp dự đoán, làm tròn từ manifest):

| Chỉ số ảnh | Nhãn thật | Dự đoán | Confidence | Kết quả |
|---|---|---|---|---|
| 8268 | police van | police van | 0,9741 | Đúng |
| 8132 | butcher shop | barbershop | 0,1726 | Sai |
| 9034 | walking stick | walking stick | 0,6256 | Đúng |
| 5650 | steel arch bridge | water tower | 0,5523 | Sai |

**Quan sát từ hình.** Ở ảnh `police van` (#8268), CLS map có các vùng nóng trên thân xe, trong khi rollout trải rộng hơn sang vùng lân cận. Ở `walking stick` (#9034), cả hai map tập trung gần vùng sáng ở giữa-bên phải ảnh và ít hơn ở phần nền tối. Với ảnh sai `butcher shop` (#8132), rollout vẫn tô nổi vùng trung tâm/phần quầy phía dưới nhưng dự đoán là `barbershop`; việc có vùng nóng không bảo đảm phân loại đúng. Trường hợp `steel arch bridge` (#5650) bị đoán thành `water tower` cũng cho thấy một dự đoán sai vẫn có confidence đáng kể trong tập minh họa.

Đây là nhận xét định tính trên các ảnh được chọn, không phải kết quả đo định vị vật thể hoặc so sánh độ tốt của hai phương pháp. Heatmap không tự chứng minh vùng nào gây ra quyết định phân loại; mô hình chưa được kiểm tra bằng can thiệp hoặc che vùng trong TASK-008. Bài [Abnar và Zuidema](https://aclanthology.org/2020.acl-main.385/) cũng phân tích hạn chế của attention thô khi thông tin đã trộn qua nhiều layer. Kết quả hình và code đang chờ TV1 review tại [PR #6](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/6) trước khi đánh dấu TASK-008 Hoàn thành.

### 6.4. Grad-CAM cho CNN (TV3, nếu làm)

Chưa có. Phần mở rộng, chỉ làm nếu còn thời gian theo thứ tự cắt việc trong [docs/03_plan.md](../docs/03_plan.md).

## 7. Phân tích lỗi và giới hạn

*Người viết: TV5; mỗi người bổ sung giới hạn của phần mình.*

Cần có: overfit (so sánh đường cong train và validation); lớp hay bị nhầm và ví dụ ảnh sai; ảnh 64 × 64 mất chi tiết; giới hạn tính toán. Bắt buộc có đoạn về độ tin cậy: tập test 10.000 ảnh cho sai số khoảng ±0,5 điểm phần trăm và chỉ chạy 1 seed, nên chênh lệch giữa ViT và CNN dưới khoảng 1–1,5 điểm không đủ để kết luận mô hình nào tốt hơn (nếu chạy 3 seed thì cập nhật câu này).

Giới hạn phần TV2: kiểm chứng chức năng và sinh hình attention được chạy trên CPU; chưa chạy attention trên CUDA/AMP hoặc benchmark tốc độ/VRAM. Đã có hình thật từ checkpoint được bàn giao, nhưng nhóm ảnh chọn cân bằng đúng/sai không đại diện cho accuracy toàn bộ test. Bản đồ có lưới patch thô, được nội suy và chuẩn hóa riêng; chưa có kiểm chứng định vị hoặc quan hệ nhân quả. Các test truyền gradient và khớp hai nhánh không thay thế đánh giá accuracy hoặc phân tích overfit của các phần thực nghiệm còn lại.

TV5 và các thành viên bổ sung phân tích lỗi, giới hạn ngân sách huấn luyện và độ tin cậy của kết quả sau khi hoàn thành thí nghiệm. Không kết luận ưu thế giữa hai mô hình khi chưa có số liệu.

## 8. Mã nguồn, hướng dẫn cài đặt, chạy và demo

*Người viết: TV1; TV5 bổ sung phần demo.*

**Mã nguồn** (đề yêu cầu nộp kèm):

| File | Chức năng | Người viết | Trạng thái |
|---|---|---|---|
| `src/utils.py` | Đọc config, seed, đếm tham số, lưu checkpoint an toàn | TV1 | Có |
| `scripts/prepare_data.py` | Tải, chia tập, tạo cache | TV1 | Có |
| `src/data.py` | DataLoader và augmentation | TV1 | Có |
| `src/models/vit.py`, `src/models/__init__.py` | ViT tự cài, `build_model` | TV2 | Có |
| `src/models/cnn.py` | ResNet nhỏ, `match_param_count` | TV3 | Chưa có |
| `src/train.py` | Vòng lặp train | TV4 | Chưa có |
| `src/evaluate.py`, `scripts/error_analysis.py`, `src/compare.py` | Đánh giá, phân tích lỗi, so sánh | TV5 | Chưa có |
| `src/attention.py` | CLS attention, rollout và CLI từ checkpoint | TV2 | Có code, 12 ảnh thật; chờ review TASK-008 |
| `app/demo.py` | Demo Gradio | TV5 | Chưa có |

**Cài đặt và chạy.**

Chưa hoàn thiện phần bàn giao cuối. Hướng dẫn đang chạy được nằm ở [README](../README.md), gồm cài môi trường, chuẩn bị dữ liệu và kiểm thử. Có thể chạy riêng test ViT mà không tải bộ dữ liệu:

```bash
python -m pytest tests/test_models.py -q -W error
```

TV1 và TV5 bổ sung lệnh train, đánh giá, demo và link checkpoint sau khi đã chạy thành công; hiện chưa có các sản phẩm đó.

## 9. Kết luận và hướng phát triển

*Người viết: TV1.* Chưa có.

Cần có: trả lời hai câu hỏi của đồ án (ViT so với CNN cùng số tham số trong ngân sách 50 epoch; ViT nhìn vào vùng nào khi dự đoán), chỉ dựa trên số liệu ở mục 4–7; hướng phát triển.

## 10. Tài liệu tham khảo

1. Alexey Dosovitskiy và cộng sự (2020). [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929). arXiv:2010.11929. Cơ sở kiến trúc ViT; cấu hình trong đồ án được trình bày riêng tại mục 3.1.
2. Samira Abnar và Willem Zuidema (2020). [Quantifying Attention Flow in Transformers](https://aclanthology.org/2020.acl-main.385/). ACL, trang 4190–4197. Cơ sở phương án attention rollout tại mục 6.2.

3. Ya Le và Xuan Yang (2015). Tiny ImageNet Visual Recognition Challenge. Báo cáo môn CS231n, Đại học Stanford. Nguồn dữ liệu tại mục 2.
4. Hongyi Zhang và cộng sự (2018). [mixup: Beyond Empirical Risk Minimization](https://arxiv.org/abs/1710.09412). ICLR. Dùng ở mục 3.3.
5. Sangdoo Yun và cộng sự (2019). [CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features](https://arxiv.org/abs/1905.04899). ICCV. Dùng ở mục 3.3.
6. Ramprasaath R. Selvaraju và cộng sự (2017). [Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization](https://arxiv.org/abs/1610.02391). ICCV. Chỉ giữ nếu làm mục 6.4.

*TV5 rà lại danh mục khi ghép bản cuối; tài liệu nào không được dẫn trong bài thì bỏ.*
