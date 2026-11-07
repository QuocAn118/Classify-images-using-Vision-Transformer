# AGENT SPEC: ViT Image Classification trên Tiny ImageNet (Đề số 9 - Môn Học sâu)

> Tài liệu này là yêu cầu đầy đủ cho AI coding agent. Hãy đọc hết trước khi code. Làm theo thứ tự các giai đoạn. Không bỏ qua phần "Tiêu chí hoàn thành".

---

## 1. Tổng quan đề tài

- **Môn:** Học sâu (Deep Learning). **Nhóm mô hình:** Transformer. **Đề số:** 9.
- **Task:** Classification (phân loại ảnh, 200 lớp).
- **Dataset:** Tiny ImageNet (https://www.kaggle.com/c/tiny-imagenet). Đề gốc cho phép Tiny ImageNet **hoặc** CIFAR-100. Nhóm chọn Tiny ImageNet và chỉ chuyển sang CIFAR-100 theo quy tắc ở mục 20.
- **Model:** Vision Transformer (ViT) = patch embedding + Transformer encoder.
- **Extension bắt buộc:**
  1. So sánh ViT với CNN **có cùng số lượng tham số** (sai lệch cho phép <= 5%).
  2. **Trực quan hóa attention** của ViT.
- **Lưu ý:** Đề KHÔNG liên quan đến deepfake (giáo viên đã xóa). Không làm phần deepfake.
- **Nhóm:** 5 người. **Hạn nộp:** 20/11/2026, nhóm đặt mục tiêu nộp 19/11/2026. Không có vấn đáp.

### Mức ưu tiên

| Mức | Nội dung |
|---|---|
| **Đề gốc yêu cầu** | ViT, Tiny ImageNet hoặc CIFAR-100, so sánh với CNN cùng số tham số, trực quan hóa attention |
| **Báo cáo cần có** | Vấn đề và phạm vi, dữ liệu mẫu và mô tả, mã nguồn, hướng dẫn cài đặt/chạy, demo, kết quả so với baseline, phân tích lỗi và giới hạn |
| **Nhóm tự thêm, làm nếu còn thời gian** | Grad-CAM, FLOPs, 3 seed, ViT pretrained, ablation, attention theo head và theo layer |
| **Có thể bỏ** | EMA, ECE, TensorBoard, notebook khám phá dữ liệu |

Khi thiếu thời gian, cắt phần nhóm tự thêm theo thứ tự ở mục 20 và giữ nguyên yêu cầu của đề gốc.

## 2. Mục tiêu đo lường

| Chỉ số | Yêu cầu |
|---|---|
| Top-1 accuracy (tập test) | Báo cáo cho ViT và CNN |
| Top-5 accuracy (tập test) | Báo cáo cho ViT và CNN |
| Số tham số | ViT và CNN chênh nhau <= 5% |
| Thời gian train/epoch, tốc độ inference | Báo cáo thêm trong bảng so sánh; thêm FLOPs nếu còn thời gian |
| Mục tiêu tham khảo | ViT from scratch >= 40% Top-1; CNN baseline >= 50% Top-1; ViT pretrained fine-tune >= 75% (chỉ để làm mốc tham chiếu) |

Các con số mục tiêu chỉ là ước lượng; không được gian lận hay chỉnh số liệu. Nếu kết quả thấp hơn, ghi trung thực và phân tích nguyên nhân.

## 3. Môi trường và ràng buộc

- Python 3.10+, PyTorch >= 2.0, torchvision. Thư viện khác cho phép: numpy, pandas, matplotlib, scikit-learn, tqdm, pyyaml, Pillow, gradio (demo), `thop` hoặc `fvcore` (FLOPs, tùy chọn), `timm` (CHỈ dùng cho bản pretrained tham chiếu và RandAugment/Mixup nếu cần).
- Hỗ trợ GPU (CUDA) và tự động fallback CPU. Dùng mixed precision (`torch.autocast`) khi có GPU.
- Train trên máy có GPU 6GB VRAM của một thành viên nhóm; Colab/Kaggle là phương án dự phòng. Batch size mặc định 128; đo VRAM đỉnh trước khi train thật, nếu không vừa thì dùng batch 64 và lr ViT 2,5e-4. ViT và CNN luôn dùng cùng batch.
- Đặt `seed` cố định (mặc định 42) cho random, numpy, torch để tái lập kết quả.
- **ViT chính phải tự cài đặt** (không gọi `timm.create_model` cho mô hình chính). `timm` chỉ dùng cho mốc pretrained.
- Mã sạch, có type hint và docstring ngắn, cấu hình qua file YAML, không hardcode đường dẫn.
- Nếu một thư viện chưa cài được (không có mạng), dùng phương án thay thế bằng PyTorch thuần và ghi chú trong README.

## 4. Cấu trúc thư mục dự án

```
Classify-images-using-Vision-Transformer/   # thư mục gốc repo là gốc project
├── README.md                  # hướng dẫn cài đặt/chạy (tiếng Việt)
├── requirements.txt
├── .gitignore                 # bỏ qua data/ và outputs/checkpoints/
├── configs/
│   ├── vit_small.yaml
│   ├── cnn_baseline.yaml
│   └── vit_pretrained.yaml
├── data/                      # dữ liệu tải về (không commit)
├── src/
│   ├── data.py                # tải, chuẩn bị, DataLoader, augmentation
│   ├── models/
│   │   ├── vit.py             # ViT tự cài
│   │   ├── cnn.py             # ResNet nhỏ tự cài, tham số ~ khớp ViT
│   │   └── pretrained.py      # fine-tune ViT pretrained (mốc tham chiếu)
│   ├── train.py               # vòng lặp huấn luyện
│   ├── evaluate.py            # đánh giá, confusion matrix, per-class acc
│   ├── attention.py           # attention map + attention rollout
│   ├── gradcam.py             # Grad-CAM cho CNN (so sánh, tùy chọn)
│   ├── compare.py             # bảng so sánh ViT vs CNN
│   └── utils.py               # seed, đếm tham số, FLOPs, logging, checkpoint
├── scripts/
│   ├── prepare_data.py
│   ├── run_all.sh
│   └── error_analysis.py
├── tests/
│   └── test_models.py
├── app/
│   └── demo.py                # Gradio demo
├── notebooks/
│   └── explore_data.ipynb     # (tùy chọn)
├── outputs/
│   ├── checkpoints/
│   ├── logs/
│   ├── figures/
│   └── results/               # json/csv kết quả
└── report/
    └── report.md              # báo cáo cuối
```

## 5. Giai đoạn 1: Chuẩn bị dữ liệu (`src/data.py`, `scripts/prepare_data.py`)

### 5.1 Cấu trúc Tiny ImageNet gốc

```
tiny-imagenet-200/
├── wnids.txt                  # 200 mã lớp (wnid)
├── words.txt                  # wnid -> tên lớp
├── train/<wnid>/images/*.JPEG # 500 ảnh/lớp
├── val/images/*.JPEG          # 10.000 ảnh, KHÔNG chia theo lớp
├── val/val_annotations.txt    # tên_ảnh \t wnid \t bbox...
└── test/images/*.JPEG         # 10.000 ảnh, KHÔNG có nhãn
```

### 5.2 Việc cần làm

1. Viết `prepare_data.py` để:
   - Tải/giải nén dữ liệu. Nếu không có API Kaggle, đọc từ đường dẫn người dùng đặt trong config (`data.root`) và in hướng dẫn tải thủ công (đăng nhập Kaggle, Join Competition, tải zip). Có thể dùng `kaggle competitions download -c tiny-imagenet` khi có `kaggle.json`.
   - Sắp xếp lại `val/` thành `val/<wnid>/*.JPEG` dựa vào `val_annotations.txt`.
   - Kiểm tra đủ 200 lớp, 100.000 ảnh train, 10.000 ảnh val; in thống kê.
2. **Chia dữ liệu (rất quan trọng, tránh rò rỉ):**
   - `train` gốc -> **90% train / 10% validation** (chia có phân tầng theo lớp, seed cố định). Validation dùng để chọn siêu tham số và early stopping.
   - `val` gốc (10.000 ảnh, có nhãn) -> dùng làm **tập TEST cuối cùng**. Chỉ đánh giá trên test một lần sau khi chốt cấu hình.
   - Tập `test` gốc không có nhãn -> bỏ qua.
3. Chuẩn hóa ảnh với mean/std của Tiny ImageNet (tính từ tập train) hoặc ImageNet (0.485, 0.456, 0.406 / 0.229, 0.224, 0.225).
4. Xuất `outputs/results/dataset_stats.json` (số ảnh mỗi tập, số lớp) và lưu 1 hình lưới 5x5 ảnh mẫu kèm tên lớp (`outputs/figures/samples.png`).
5. `img_size`, `patch_size`, `num_classes` và tên dataset phải nằm trong config, không hardcode, để đổi sang CIFAR-100 (ảnh 32x32, patch 4, 100 lớp, tải qua `torchvision`) mà không phải sửa code. Với CIFAR-100: chia train 90/10 như trên và dùng tập test có sẵn làm TEST.

### 5.3 Augmentation

- **Train:** RandomCrop(64, padding=4) hoặc RandomResizedCrop(64, scale=(0.6,1.0)), RandomHorizontalFlip, RandAugment (hoặc TrivialAugment), RandomErasing (p=0.25).
- **Mixup (alpha=0.8) và CutMix (alpha=1.0)** áp dụng ở mức batch, có thể bật/tắt qua config.
- **Label smoothing:** 0.1.
- **Val/Test:** chỉ ToTensor + Normalize.
- DataLoader: `num_workers` theo CPU, `pin_memory=True`, `persistent_workers=True`.

## 6. Giai đoạn 2: Cài đặt ViT (`src/models/vit.py`)

Tự cài đặt bằng PyTorch thuần, gồm các module:

1. **PatchEmbedding:** `Conv2d(in=3, out=embed_dim, kernel=patch, stride=patch)` -> flatten -> (B, N, D). Với ảnh 64x64, patch 8 -> N = 64 token.
2. **CLS token** (tham số học được) ghép vào đầu chuỗi.
3. **Learnable positional embedding** kích thước (1, N+1, D), khởi tạo `trunc_normal_(std=0.02)`.
4. **TransformerEncoderBlock** (Pre-LayerNorm):
   - `x = x + DropPath(MHSA(LN(x)))`
   - `x = x + DropPath(MLP(LN(x)))`
   - MHSA tự cài (qkv linear, scaled dot-product, softmax, proj). **Phải trả về được attention weights** (tham số `return_attn=True`) để vẽ attention. Không dùng `F.scaled_dot_product_attention` fused ở chế độ cần lấy attention (hoặc có nhánh tính tường minh khi cần lấy attention).
   - MLP: Linear(D, D*mlp_ratio) -> GELU -> Dropout -> Linear -> Dropout.
   - Stochastic depth (DropPath) tăng tuyến tính theo độ sâu, tối đa `drop_path_rate` (0.1).
5. **Classification head:** LayerNorm cuối -> lấy CLS token -> Linear(D, 200).
6. Khởi tạo trọng số: Linear dùng `trunc_normal_(std=0.02)`, bias = 0; LayerNorm weight=1, bias=0.

### Cấu hình mặc định `vit_small.yaml`

| Siêu tham số | Giá trị |
|---|---|
| img_size | 64 |
| patch_size | 8 |
| embed_dim | 256 |
| depth | 8 |
| num_heads | 8 |
| mlp_ratio | 4 |
| dropout | 0.0 - 0.1 |
| drop_path_rate | 0.1 |
| num_classes | 200 |

Ước lượng ~6-7 triệu tham số; in số tham số chính xác khi chạy. Cho phép biến thể `patch_size=4` (256 token, nặng hơn) và `vit_tiny` (dim 192, depth 6, heads 3) để ablation.

### Kiểm thử đơn vị (viết `tests/test_models.py`)

- Forward shape: input (2,3,64,64) -> output (2,200).
- `return_attn=True` trả về list attention shape (B, heads, N+1, N+1) mỗi layer, mỗi hàng tổng = 1 (sai số 1e-4). Test chạy ở `model.eval()`, và attention trả về phải lấy **trước** dropout.
- Đếm tham số khớp với tính tay.

## 7. Giai đoạn 3: Baseline CNN cùng số tham số (`src/models/cnn.py`)

- Tự cài **ResNet nhỏ** (BasicBlock, BatchNorm, ReLU, global average pooling, FC 200 lớp), phù hợp ảnh 64x64 (conv đầu 3x3 stride 1, không maxpool lớn).
- **Điều chỉnh độ rộng/độ sâu (width multiplier, số block) sao cho tổng số tham số chênh lệch <= 5% so với ViT.** Viết hàm `match_param_count(target_params)` tự tìm cấu hình phù hợp, in kết quả.
- Dùng cùng pipeline dữ liệu, cùng số epoch, cùng augmentation (để so sánh công bằng). **Kết quả so sánh chính dùng AdamW cho cả hai mô hình**; có thể tinh chỉnh learning rate riêng cho CNN và ghi rõ trong báo cáo. SGD (momentum 0.9, lr 0.1, wd 5e-4) chỉ là thí nghiệm tham khảo nếu còn thời gian.
- Ghi bảng: params, thời gian/epoch, VRAM đỉnh, tốc độ inference (ảnh/giây), và FLOPs nếu còn thời gian. Báo cáo phải nêu rõ cùng số tham số không có nghĩa là cùng chi phí tính toán.

## 8. Giai đoạn 4: Huấn luyện (`src/train.py`)

### Công thức huấn luyện ViT (from scratch)

- Optimizer: **AdamW**, lr đỉnh 1e-3 cho batch 256, scale tuyến tính theo batch (**batch mặc định 128 thì lr = 5e-4**), betas (0.9, 0.999), weight decay 0.05 (không áp dụng cho bias, LayerNorm, pos_embed, cls_token).
- Scheduler: **warmup 10 epoch** tuyến tính, sau đó **cosine decay** về 1e-5.
- Epoch: 100 (tối thiểu 50). Muốn chạy ngắn thì dùng `--epochs N`; `--quick` chỉ dùng cho smoke test vài batch.
- Loss: CrossEntropy với label smoothing 0.1 (tự chuyển sang SoftTargetCE khi bật Mixup/CutMix).
- Gradient clipping: max_norm = 1.0.
- Mixed precision (AMP) khi có GPU.
- EMA của trọng số (tùy chọn, decay 0.999).

### Yêu cầu chức năng

- CLI: `python -m src.train --config configs/vit_small.yaml [--quick] [--epochs N] [--seed S] [--resume path]`.
- Mỗi epoch ghi log: train loss/acc, val loss/Top-1/Top-5, lr, thời gian. Lưu CSV `outputs/logs/<run_name>.csv` và (tùy chọn) TensorBoard. Khi bật Mixup/CutMix, train acc không còn ý nghĩa; nhận xét và chọn checkpoint dựa trên validation.
- Lưu checkpoint tốt nhất theo val Top-1 và checkpoint cuối; hỗ trợ `--resume`.
- Early stopping (patience 15) tùy chọn.
- Vẽ đường cong loss/accuracy -> `outputs/figures/<run_name>_curves.png`.
- Chạy được trên cả CPU với `--quick` (vài batch) để kiểm tra pipeline (smoke test).

### Ablation (chạy nếu còn thời gian, mỗi lần 1 thay đổi)

1. Patch size: 4 vs 8 vs 16.
2. Có/không Mixup+CutMix.
3. Độ sâu: 4 vs 8 vs 12 layer.
4. Có/không RandAugment.

Ghi mọi kết quả vào `outputs/results/ablation.csv`. Chỉ so sánh ablation trên **validation**, mỗi lần chạy 50 epoch, làm lần lượt theo thứ tự trên.

## 9. Giai đoạn 5: Mốc tham chiếu pretrained (`src/models/pretrained.py`) - làm nếu còn thời gian

- Fine-tune **ViT/DeiT-Small pretrained trên ImageNet-1k** (qua `timm`), resize ảnh lên 224x224 (hoặc nội suy positional embedding cho kích thước nhỏ hơn như 112) và thay head thành 200 lớp.
- Fine-tune 5-10 epoch, lr thấp (1e-4 cho backbone, 1e-3 cho head), layer-wise lr decay (tùy chọn).
- **Mục đích:** chỉ làm mốc tham chiếu, ghi rõ trong báo cáo là mô hình này KHÔNG cùng số tham số với baseline nên không nằm trong so sánh công bằng chính.
- Nếu không có mạng để tải trọng số pretrained, bỏ qua phần này và ghi chú rõ.

## 10. Giai đoạn 6: Đánh giá và phân tích lỗi (`src/evaluate.py`, `scripts/error_analysis.py`)

Chạy trên tập **test** (val gốc) với checkpoint tốt nhất, cho ViT và CNN:

1. Top-1, Top-5 accuracy.
2. **Per-class accuracy** (200 lớp), lưu CSV; liệt kê 10 lớp tốt nhất và 10 lớp tệ nhất kèm tên lớp (dùng `words.txt`).
3. **Confusion matrix**: do 200 lớp quá lớn, vẽ heatmap tổng thể và bảng **top 20 cặp lớp bị nhầm nhiều nhất**.
4. Lưu lưới 20 ảnh dự đoán sai tiêu biểu (nhãn thật vs dự đoán, độ tin cậy) -> `outputs/figures/errors_<model>.png`.
5. Phân tích ngắn (viết vào báo cáo): vì sao nhầm (giống chó, côn trùng, ảnh mờ do 64x64), ViT thua/thắng CNN ở nhóm lớp nào.
6. Kiểm tra tính hiệu chỉnh (calibration): ECE, tùy chọn.

## 11. Giai đoạn 7: Trực quan hóa attention (`src/attention.py`)

1. **CLS-attention map:** lấy attention từ CLS token tới các patch ở layer cuối, trung bình các head, reshape theo lưới `img_size // patch_size` (không hardcode; patch 8 trên ảnh 64 cho lưới 8x8), upsample bilinear lên kích thước ảnh, phủ lên ảnh gốc (heatmap alpha 0.5).
2. **Attention rollout** (Abnar & Zuidema, 2020): với mỗi layer, `A' = 0.5*A_mean + 0.5*I`, chuẩn hóa hàng, nhân dồn các layer, lấy hàng CLS. Vẽ heatmap tương tự.
3. **Theo head (nếu còn thời gian):** lưới các head của layer cuối cho cùng một ảnh.
4. **Theo layer (nếu còn thời gian):** attention của CLS qua các layer từ nông tới sâu.
5. Chọn tối thiểu 12 ảnh test (gồm cả dự đoán đúng và sai, nhiều lớp khác nhau); mỗi ảnh hiển thị: ảnh gốc | rollout | CLS-attn layer cuối.
6. **So sánh với CNN (nếu còn thời gian, đề gốc không yêu cầu):** Grad-CAM cho CNN (layer conv cuối) trên cùng các ảnh -> hình ghép ViT-rollout vs CNN Grad-CAM (`outputs/figures/attn_vs_gradcam.png`). Bình luận ngắn xem mô hình nhìn vào vùng nào.
7. Lưu tất cả hình vào `outputs/figures/attention/`.

## 12. Giai đoạn 8: So sánh ViT vs CNN (`src/compare.py`)

Sinh `outputs/results/comparison.md` và `comparison.csv` với bảng:

| Mô hình | Params | FLOPs | Top-1 | Top-5 | Thời gian/epoch | Inference (img/s) | Ghi chú |
|---|---|---|---|---|---|---|---|
| ViT-small (from scratch) | | | | | | | |
| ResNet-nhỏ (cùng params) | | | | | | | |
| ViT pretrained (tham chiếu) | | | | | | | không cùng params |

Kèm biểu đồ cột Top-1 và đường cong val accuracy chồng nhau của ViT và CNN. Chạy mỗi cấu hình chính với **3 seed** (42, 43, 44) nếu thời gian cho phép, báo cáo mean ± std.

## 13. Giai đoạn 9: Demo (`app/demo.py`)

- Gradio (hoặc Streamlit): người dùng upload ảnh -> hiển thị **Top-5 dự đoán (tên lớp + xác suất)** của ViT và CNN, kèm **ảnh attention rollout** của ViT.
- Tự resize ảnh về 64x64. Nạp checkpoint từ `outputs/checkpoints/`.
- Chạy bằng `python app/demo.py`; ghi cách chạy trong README. Phải chạy được trên CPU.
- Chuẩn bị 5-10 ảnh mẫu trong `app/examples/` (lấy từ tập test; dùng ảnh có giấy phép phù hợp).

## 14. Sản phẩm bàn giao (checklist)

- [ ] Mã nguồn đầy đủ theo cấu trúc mục 4.
- [ ] `README.md` (tiếng Việt): giới thiệu, cài đặt, tải dữ liệu, lệnh train/eval/demo, cấu trúc thư mục, kết quả tóm tắt.
- [ ] `requirements.txt` (ghim phiên bản chính).
- [ ] Mẫu đăng ký đề tài đã nộp (mục 21).
- [ ] Checkpoint ViT, CNN (và pretrained nếu có), lưu ngoài git (Google Drive hoặc Kaggle Dataset) và ghi link trong README.
- [ ] Bảng so sánh và biểu đồ (mục 12).
- [ ] Hình attention (mục 11), và Grad-CAM nếu có làm.
- [ ] Dữ liệu mẫu: hình lưới `samples.png` và 5-10 ảnh thật trong `app/examples/`.
- [ ] Phân tích lỗi (mục 10).
- [ ] Demo chạy được (mục 13).
- [ ] `report/report.md` đủ các mục ở phần 15.
- [ ] Test đơn vị cơ bản chạy qua (`pytest`).

## 15. Cấu trúc báo cáo cuối (`report/report.md`, tiếng Việt)

Đề yêu cầu báo cáo gồm: báo cáo vấn đề và phạm vi; dữ liệu mẫu và mô tả; mã nguồn; hướng dẫn cài đặt/chạy; demo; kết quả so sánh với baseline; phân tích lỗi và giới hạn.

1. **Vấn đề và phạm vi:** bài toán, vì sao ViT, phạm vi bắt buộc và mở rộng.
2. **Dữ liệu:** nguồn, quy mô, cách chia train/val/test, ảnh mẫu, thống kê.
3. **Phương pháp:** kiến trúc ViT (sơ đồ), baseline CNN, cách khớp số tham số, công thức huấn luyện, augmentation.
4. **Thực nghiệm:** cấu hình, kết quả chính, đường cong học, ablation.
5. **So sánh ViT vs CNN:** bảng ở mục 12, nhận xét (ViT thiếu inductive bias nên cần nhiều dữ liệu/augmentation).
6. **Trực quan hóa attention:** hình và nhận xét.
7. **Phân tích lỗi và giới hạn:** overfit, ảnh 64x64 mất chi tiết, giới hạn tính toán, đe dọa tính hợp lệ (ví dụ chỉ chạy ít seed).
8. **Hướng dẫn cài đặt/chạy và demo.**
9. **Kết luận và hướng phát triển.**
10. **Tài liệu tham khảo:** ViT (Dosovitskiy et al., 2020), DeiT (Touvron et al., 2021), Tiny ImageNet (Stanford CS231n), Attention Rollout (Abnar & Zuidema, 2020), Grad-CAM (Selvaraju et al., 2017), Mixup, CutMix.

## 16. Kế hoạch thực hiện cho agent (thứ tự ưu tiên; phân công và lịch ở mục 19-20)

1. Dựng khung thư mục, `requirements.txt`, `.gitignore`, `utils.py`.
2. `prepare_data.py` + `data.py`, kiểm tra thống kê và ảnh mẫu.
3. `vit.py` + test đơn vị; chạy smoke test `--quick` trên vài batch.
4. `cnn.py` + `match_param_count`; xác nhận chênh lệch tham số <= 5%.
5. `train.py`; train CNN rồi ViT (chạy nền, ghi log).
6. `evaluate.py`, `error_analysis.py`.
7. `attention.py`.
8. `compare.py`. Nếu còn thời gian, làm thêm theo thứ tự: `gradcam.py`, FLOPs, 3 seed, pretrained, ablation.
9. `demo.py`.
10. `README.md` và `report/report.md`.

## 17. Quy tắc chất lượng và trung thực

- **Không rò rỉ dữ liệu:** không dùng tập test để chọn siêu tham số hay checkpoint.
- **Không bịa số liệu.** Mọi con số trong báo cáo phải lấy từ file log/kết quả thực tế do code sinh ra. Nếu chưa chạy xong, ghi "chưa có".
- So sánh công bằng: cùng dữ liệu, cùng split, cùng ngân sách epoch; ghi rõ khác biệt (optimizer, lr) nếu có.
- Báo cáo mọi hạn chế trung thực (ít seed, ít epoch, giới hạn GPU).
- Mỗi giai đoạn xong phải chạy thử để chắc code hoạt động trước khi sang giai đoạn sau; sửa lỗi thay vì bỏ qua.
- Nếu gặp vướng mắc không tự giải quyết được (ví dụ không tải được dataset), dừng lại và nêu rõ cần người dùng làm gì, không đoán mò.

## 18. Tiêu chí hoàn thành (Definition of Done)

1. `python scripts/prepare_data.py` chuẩn bị đúng dữ liệu (200 lớp, 100k train, 10k val gốc làm test).
2. `python -m src.train --config configs/vit_small.yaml` train xong, sinh checkpoint và log.
3. `python -m src.train --config configs/cnn_baseline.yaml` train xong; số tham số chênh <= 5% so với ViT.
4. `python -m src.evaluate` sinh Top-1/Top-5, per-class accuracy, confusion matrix cho cả hai mô hình.
5. `python -m src.attention` sinh hình attention rollout (>= 12 ảnh). Grad-CAM không nằm trong tiêu chí bắt buộc.
6. `python -m src.compare` sinh bảng so sánh.
7. `python app/demo.py` mở được demo.
8. `pytest` pass.
9. Báo cáo `report/report.md` đầy đủ, số liệu khớp với file kết quả.
10. Mẫu đăng ký đề tài đã nộp.

## 19. Phân công 5 người

| Thành viên | Vai trò | Phụ trách | Phần báo cáo (mục 15) |
|---|---|---|---|
| TV1 | Trưởng nhóm, dữ liệu | Mẫu đăng ký, khung repo, `utils.py`, `prepare_data.py`, `data.py`, `README.md`, duyệt PR | 1, 2, 8, 9 |
| TV2 | ViT và attention | `vit.py`, `tests/test_models.py`, `attention.py` | 3 (ViT), 6 |
| TV3 | CNN | `cnn.py`, `match_param_count`, đo thời gian/VRAM/tốc độ, `gradcam.py` nếu làm | 3 (CNN), 6 (Grad-CAM nếu có) |
| TV4 | Huấn luyện | `train.py`, `run_all.sh`, chạy thí nghiệm, quản lý checkpoint, `pretrained.py` nếu làm | 4 |
| TV5 | Đánh giá và demo | `evaluate.py`, `error_analysis.py`, `compare.py`, `demo.py`, ghép báo cáo | 5, 7, 10 |

Train chính chạy lần lượt trên máy GPU của một thành viên (nên là TV4); các thành viên khác dùng tài khoản Kaggle/Colab của mình nếu cần chạy thêm song song. Mỗi PR có một người khác review trước khi merge.

## 20. Lịch và quy tắc cắt việc

| Ngày | Việc | Phụ trách chính |
|---|---|---|
| 7-8/11 | Nộp mẫu đăng ký, dựng repo, thống nhất giao diện (chữ ký `forward`, định dạng checkpoint, cột log CSV, cấu trúc JSON kết quả), tải dữ liệu | TV1, cả nhóm |
| 9-10/11 | Xong ViT, CNN, `train.py`; chạy thông `--quick` và sinh checkpoint thử | TV2, TV3, TV4 |
| 11/11 | Đo thời gian mỗi epoch, chốt số thí nghiệm, bắt đầu train thật | TV4 |
| 11-14/11 | Train ViT và CNN; song song làm đánh giá, attention, demo bằng checkpoint thử | TV4, rồi TV2, TV3, TV5 |
| 14-16/11 | Làm thêm nếu kịp; chốt checkpoint rồi đánh giá trên test một lần | TV4, TV5 |
| 16/11 | **Dừng mọi thí nghiệm** | Cả nhóm |
| 17-18/11 | Điền số liệu thật vào báo cáo, phân tích lỗi, hoàn thiện demo | TV5, cả nhóm |
| 19/11 | Dò số liệu, chạy lại trên máy sạch, nộp bài | Cả nhóm |
| 20/11 | Dự phòng | |

Quy tắc cắt việc:

- **Thứ tự cắt khi trễ:** ablation, pretrained, 3 seed, FLOPs, Grad-CAM.
- **Chậm train:** nếu đến 13/11 ViT chưa train xong, giảm xuống 50 epoch và ghi rõ trong báo cáo.
- **Kẹt dữ liệu hoặc GPU:** nếu đến 10/11 chưa chạy được Tiny ImageNet, chuyển sang CIFAR-100.

## 21. Bản nháp mẫu đăng ký đề tài

1. **Tên đề tài:** Phân loại ảnh 200 lớp trên Tiny ImageNet bằng Vision Transformer, so sánh với CNN cùng số tham số và trực quan hóa attention.
2. **Hướng chính:** AI dự đoán.
3. **Người sử dụng và vấn đề:** Sinh viên và người nghiên cứu thị giác máy tính cần chọn giữa ViT và CNN khi dữ liệu ít, ảnh độ phân giải thấp và số tham số bị giới hạn. Khó khăn hiện tại: ViT thường cần nhiều dữ liệu, các so sánh hay dùng mô hình khác cỡ nên khó công bằng, và khó biết mô hình đang nhìn vào vùng nào của ảnh.
4. **Mục tiêu:** Có mô hình ViT tự cài đặt và CNN baseline chênh không quá 5% số tham số. Đo Top-1 và Top-5 trên tập test, với mức tham khảo ViT >= 40% và CNN >= 50% Top-1. Có hình attention cho ít nhất 12 ảnh.
5. **Dữ liệu:** Tiny ImageNet trên Kaggle; trường dữ liệu gồm ảnh RGB 64x64 và nhãn lớp; quy mô 200 lớp, 100.000 ảnh train, 10.000 ảnh val có nhãn. Quyền sử dụng: [nhóm kiểm tra điều khoản trên trang Kaggle trước khi nộp]. Phương án thay thế: CIFAR-100.
6. **Phạm vi:** Bắt buộc gồm ViT tự cài, CNN cùng số tham số, trực quan hóa attention, demo. Mở rộng nếu còn thời gian gồm Grad-CAM, FLOPs, 3 seed, ViT pretrained, ablation.
7. **Phương pháp:** Baseline là ResNet nhỏ tự cài, khớp số tham số với ViT. Giải pháp là ViT (patch embedding + Transformer encoder) dùng AdamW, warmup + cosine, Mixup/CutMix, trực quan hóa bằng CLS attention và attention rollout.
8. **Sản phẩm:** Mô hình đã huấn luyện, demo Gradio, ảnh mẫu, mã nguồn, README, báo cáo.
9. **Đánh giá:** Chỉ số gồm Top-1, Top-5, per-class accuracy, top 20 cặp lớp nhầm nhiều nhất, số tham số, thời gian/epoch, tốc độ inference. Cách chia: train gốc 90/10 thành train/validation, val gốc làm test. Bộ tình huống: tối thiểu 12 ảnh test gồm cả dự đoán đúng và sai để xem attention, cùng 5-10 ảnh mẫu cho demo.
10. **Kế hoạch và rủi ro:** Phân công và mốc theo mục 19-20, hoàn thành trước 20/11/2026. Phụ thuộc và cách xử lý: train phụ thuộc vào máy GPU của một thành viên, nên máy bận hoặc hỏng thì chuyển sang Kaggle/Colab và giảm xuống 50 epoch; train bị ngắt thì lưu checkpoint thường xuyên, sao lưu ra ngoài máy và `--resume`; không kịp thì cắt phần mở rộng theo mục 20; không tải được dữ liệu thì chuyển sang CIFAR-100.
