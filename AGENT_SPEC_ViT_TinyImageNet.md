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
- Phải chạy được trên GPU miễn phí (Colab/Kaggle, ~12-16GB VRAM). Batch size mặc định 128.
- Đặt `seed` cố định (mặc định 42) cho random, numpy, torch để tái lập kết quả.
- **ViT chính phải tự cài đặt** (không gọi `timm.create_model` cho mô hình chính). `timm` chỉ dùng cho mốc pretrained.
- Mã sạch, có type hint và docstring ngắn, cấu hình qua file YAML, không hardcode đường dẫn.
- Nếu một thư viện chưa cài được (không có mạng), dùng phương án thay thế bằng PyTorch thuần và ghi chú trong README.

## 4. Cấu trúc thư mục dự án

```
vit-tiny-imagenet/
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
- `return_attn=True` trả về list attention shape (B, heads, N+1, N+1) mỗi layer, mỗi hàng tổng = 1 (sai số 1e-4).
- Đếm tham số khớp với tính tay.

## 7. Giai đoạn 3: Baseline CNN cùng số tham số (`src/models/cnn.py`)

- Tự cài **ResNet nhỏ** (BasicBlock, BatchNorm, ReLU, global average pooling, FC 200 lớp), phù hợp ảnh 64x64 (conv đầu 3x3 stride 1, không maxpool lớn).
- **Điều chỉnh độ rộng/độ sâu (width multiplier, số block) sao cho tổng số tham số chênh lệch <= 5% so với ViT.** Viết hàm `match_param_count(target_params)` tự tìm cấu hình phù hợp, in kết quả.
- Dùng cùng pipeline dữ liệu, cùng số epoch, cùng optimizer family, cùng augmentation (để so sánh công bằng). Có thể tinh chỉnh learning rate riêng cho CNN (SGD momentum 0.9, lr 0.1, wd 5e-4, hoặc AdamW) và ghi rõ trong báo cáo.
- Ghi bảng: params, FLOPs, thời gian/epoch, VRAM đỉnh, tốc độ inference (ảnh/giây).

## 8. Giai đoạn 4: Huấn luyện (`src/train.py`)

### Công thức huấn luyện ViT (from scratch)

- Optimizer: **AdamW**, lr đỉnh 1e-3 (batch 256; scale tuyến tính theo batch), betas (0.9, 0.999), weight decay 0.05 (không áp dụng cho bias, LayerNorm, pos_embed, cls_token).
- Scheduler: **warmup 10 epoch** tuyến tính, sau đó **cosine decay** về 1e-5.
- Epoch: 100 (tối thiểu 50; cho phép giảm xuống 20-30 để chạy thử nhanh với cờ `--quick`).
- Loss: CrossEntropy với label smoothing 0.1 (tự chuyển sang SoftTargetCE khi bật Mixup/CutMix).
- Gradient clipping: max_norm = 1.0.
- Mixed precision (AMP) khi có GPU.
- EMA của trọng số (tùy chọn, decay 0.999).

### Yêu cầu chức năng

- CLI: `python -m src.train --config configs/vit_small.yaml [--quick] [--resume path]`.
- Mỗi epoch ghi log: train loss/acc, val loss/Top-1/Top-5, lr, thời gian. Lưu CSV `outputs/logs/<run_name>.csv` và (tùy chọn) TensorBoard.
- Lưu checkpoint tốt nhất theo val Top-1 và checkpoint cuối; hỗ trợ `--resume`.
- Early stopping (patience 15) tùy chọn.
- Vẽ đường cong loss/accuracy -> `outputs/figures/<run_name>_curves.png`.
- Chạy được trên cả CPU với `--quick` (vài batch) để kiểm tra pipeline (smoke test).

### Ablation (chạy nếu còn thời gian, mỗi lần 1 thay đổi)

1. Patch size: 4 vs 8 vs 16.
2. Có/không Mixup+CutMix.
3. Độ sâu: 4 vs 8 vs 12 layer.
4. Có/không RandAugment.

Ghi mọi kết quả vào `outputs/results/ablation.csv`.

## 9. Giai đoạn 5: Mốc tham chiếu pretrained (`src/models/pretrained.py`)

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

1. **CLS-attention map:** lấy attention từ CLS token tới 64 patch ở layer cuối, trung bình các head, reshape (8x8), upsample bilinear lên 64x64, phủ lên ảnh gốc (heatmap alpha 0.5).
2. **Attention rollout** (Abnar & Zuidema, 2020): với mỗi layer, `A' = 0.5*A_mean + 0.5*I`, chuẩn hóa hàng, nhân dồn các layer, lấy hàng CLS. Vẽ heatmap tương tự.
3. **Theo head:** lưới các head của layer cuối cho cùng một ảnh.
4. **Theo layer:** attention của CLS qua các layer từ nông tới sâu.
5. Chọn tối thiểu 12 ảnh test (gồm cả dự đoán đúng và sai, nhiều lớp khác nhau); mỗi ảnh hiển thị: ảnh gốc | rollout | CLS-attn layer cuối.
6. **So sánh với CNN:** Grad-CAM cho CNN (layer conv cuối) trên cùng các ảnh -> hình ghép ViT-rollout vs CNN Grad-CAM (`outputs/figures/attn_vs_gradcam.png`). Bình luận ngắn xem mô hình nhìn vào vùng nào.
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
- [ ] Checkpoint ViT, CNN (và pretrained nếu có).
- [ ] Bảng so sánh và biểu đồ (mục 12).
- [ ] Hình attention và Grad-CAM (mục 11).
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

## 16. Kế hoạch thực hiện cho agent (thứ tự ưu tiên)

1. Dựng khung thư mục, `requirements.txt`, `utils.py`.
2. `prepare_data.py` + `data.py`, kiểm tra thống kê và ảnh mẫu.
3. `vit.py` + test đơn vị; chạy smoke test `--quick` trên vài batch.
4. `cnn.py` + `match_param_count`; xác nhận chênh lệch tham số <= 5%.
5. `train.py`; train CNN rồi ViT (chạy nền, ghi log).
6. `evaluate.py`, `error_analysis.py`.
7. `attention.py`, `gradcam.py`.
8. `compare.py`, ablation (nếu còn thời gian), pretrained (nếu có mạng).
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
5. `python -m src.attention` sinh hình attention rollout (>= 12 ảnh) và so sánh Grad-CAM.
6. `python -m src.compare` sinh bảng so sánh.
7. `python app/demo.py` mở được demo.
8. `pytest` pass.
9. Báo cáo `report/report.md` đầy đủ, số liệu khớp với file kết quả.
