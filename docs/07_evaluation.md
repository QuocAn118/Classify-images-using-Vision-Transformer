# Đánh giá, attention và so sánh

**Người giữ:** TV5 (đánh giá, so sánh), TV2 (attention). **Đầu việc:** TASK-007, TASK-008, TASK-009, TASK-012. **Code:** đã có `src/attention.py` (TASK-008 trên `thanhbinh`, chờ TV1 review tại [PR #6](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/6)); `src/evaluate.py`, `scripts/error_analysis.py`, `src/compare.py` chưa có.

## Thành phần làm gì
Đo kết quả cuối trên test, phân tích lỗi, trực quan hóa attention của ViT và sinh bảng so sánh ViT với CNN. Mọi số đều lấy từ file.

## Quy tắc đánh giá
- Top-1, Top-5 trên test; per-class accuracy; top 20 cặp lớp nhầm.
- Đánh giá test sau khi chốt cấu hình, cùng tập test cho hai mô hình.
- Ablation chỉ báo kết quả trên validation. Test chỉ dùng cho các mô hình chính cuối cùng (ViT và CNN).
- Chênh lệch dưới khoảng 1–1,5 điểm giữa hai mô hình không đủ để kết luận (xem yêu cầu chất lượng trong [01_define.md](01_define.md)).

## Hợp đồng

**Kết quả JSON** (`outputs/results/<run_name>.json`): `run_name, model, seed, params, macs, top1, top5, epoch_time_s, inference_img_per_s, peak_vram_mb`. Chưa có số thì để `null`. `<run_name>` theo quy ước ở [06_training.md](06_training.md).

Đầu vào là checkpoint theo hợp đồng ở [06_training.md](06_training.md) và mô hình theo [05_model.md](05_model.md).

## FR-005: Đánh giá và phân tích lỗi
- **Người sử dụng:** TV5.
- **Mục đích:** Có số cuối và hiểu vì sao mô hình sai.
- **Đầu vào:** Checkpoint đã chốt, tập test.
- **Luồng bình thường:** Tính chỉ số, xuất per-class accuracy, cặp lớp nhầm và lưới ảnh sai.
- **Lỗi và biên:** Checkpoint không khớp mô hình thì báo lỗi.
- **Kết quả:** JSON kết quả, CSV per-class, hình lỗi.

## FR-006: Trực quan hóa attention
- **Người sử dụng:** TV2, người đọc báo cáo.
- **Mục đích:** Thấy ViT nhìn vào vùng nào.
- **Đầu vào:** Checkpoint ViT, ảnh test.
- **Luồng bình thường:** Lấy attention, tính CLS map và rollout, phủ heatmap lên ảnh.
- **Quy tắc:** Chọn cả ảnh dự đoán đúng và sai, nhiều lớp khác nhau.
- **Lỗi và biên:** Lưới phải đúng với mọi `patch_size` hợp lệ.
- **Kết quả:** Hình trong `outputs/figures/attention/`.

### Hợp đồng attention (TASK-008)

Thông báo trước triển khai tại [Issue #4](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/issues/4); TV5 có thể dùng các hàm này trong demo, không cần bộ dữ liệu:

- `cls_attention_map(attns, img_size, patch_size)` và `attention_rollout(attns, img_size, patch_size)` trả tensor float32 `(B,img_size,img_size)` trong `[0,1]`. Lưới lấy từ config, bỏ token CLS trước reshape, nội suy bilinear và min-max riêng mỗi ảnh. Map hằng trả toàn 0.
- `overlay_heatmap(image, heatmap, alpha=0.5)` trả ảnh PIL RGB, heatmap `(H,W)` cùng kích thước ảnh; tự chuyển ảnh xám/alpha sang RGB.
- `explain_image(model, image, cfg)` chạy eval/inference và trả dict: `image` (PIL RGB đã resize), `logits` (tensor CPU `(num_classes,)`), `cls_map`, `rollout_map` (tensor CPU `(H,W)`). Chuẩn hóa bằng `cfg.data.mean/std` và dùng `return_attn=True`.
- `load_vit_checkpoint(path, device="cpu", expected_sha256=None)` nạp với `weights_only=True`, strict state dict, trả `(model_eval, metadata)`. Metadata có `config`, `class_names`, `epoch`, `seed`, `best_val_top1`, `path`, `sha256`; không nạp config hoặc tên lớp từ file ngoài checkpoint.
- CLI `python -m src.attention --checkpoint PATH`: mặc định dùng cache `val`; chỉ đọc test khi chỉ định `--split test`, checkpoint đã được người chạy chốt. Có `--cache-dir`, `--class-names`, `--num-images` (mặc định 12), `--scan-limit` (512), `--seed` (42), `--device` (`cpu`/`cuda`), `--output-dir`, `--expected-sha256`.
- Chọn mẫu có seed cố định, cân bằng đúng/sai và ưu tiên nhãn chưa chọn; không đủ ảnh hoặc thiếu một nhóm thì báo lỗi, không coi là đạt AC-010. Manifest ghi nguồn checkpoint/split, các chỉ số ảnh, nhãn thật/dự đoán, confidence và file hình; không xuất accuracy từ tập ảnh đã chọn. Gallery, ảnh ghép, `maps.npz` và `manifest.json` là đầu ra dẫn xuất; dữ liệu gốc/checkpoint không commit.

### Bằng chứng TASK-008 ngày 2026-11-20

- Checkpoint do người dùng cung cấp, epoch 50, nạp `weights_only=True`, SHA-256 `97fbd0daa0e088b4b7d8a9c9adca4f61ba858986f00daa9669c83196a5a7b66b` khớp bàn giao TV4 trên `origin/hoangdang`. Không merge code train của TV4 trong đầu việc này.
- Chạy CPU trên cache test (val gốc Tiny ImageNet), seed chọn ảnh 42; scan 512 ảnh, chọn 12 ảnh thuộc 12 lớp, 6 đúng và 6 sai. Đây là chọn mẫu minh họa, không phải phép đo Top-1/Top-5.
- [Gallery](../outputs/figures/attention/vit_small_seed42_test/gallery.png), [manifest](../outputs/figures/attention/vit_small_seed42_test/manifest.json) và [bằng chứng kiểm tra](../outputs/results/task008_attention_checks.json). Mỗi ảnh ghép có ảnh gốc, CLS layer cuối và rollout; `maps.npz` lưu hai loại map float32 `(12,64,64)`, hữu hạn trong `[0,1]`.
- `python -m pytest -q -W error` → **73 passed**, gồm 21 ca attention. Có ma trận tính tay kiểm thứ tự rollout, head average, resize, map hằng, checkpoint, chọn mẫu và pipeline vẽ; regression cho lỗi CLI `--help` trên Windows cp1258 ([Issue #5](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/issues/5)).
- Môi trường: Python 3.12.10, torch 2.15.0+cpu; chưa kiểm tra attention trên CUDA/AMP. Code và hình chờ TV1 review, chưa tự đánh dấu Hoàn thành.

Lệnh đã chạy (chạy tại gốc repo, cần checkpoint và cache):

```bash
python -m src.attention --checkpoint outputs/checkpoints/vit_small_seed42_best.pt --split test --num-images 12 --scan-limit 512 --seed 42 --device cpu --expected-sha256 97fbd0daa0e088b4b7d8a9c9adca4f61ba858986f00daa9669c83196a5a7b66b
```

## FR-007: So sánh
- **Người sử dụng:** TV5, người đọc báo cáo.
- **Mục đích:** Có bảng so sánh ViT và CNN.
- **Đầu vào:** JSON kết quả của các mô hình.
- **Luồng bình thường:** Đọc JSON, sinh bảng và biểu đồ.
- **Quy tắc:** Mọi số lấy từ file; bảng bắt buộc có cột FLOPs/MACs (đo nếu làm được, ghi "chưa có" nếu chưa).
- **Lỗi và biên:** Số chưa có thì hiển thị "chưa có", không tự điền.
- **Kết quả:** `comparison.md`, `comparison.csv`, biểu đồ.

## Tiêu chí nghiệm thu

| Mã | Điều kiện ban đầu | Thao tác | Kết quả mong đợi |
|---|---|---|---|
| AC-009 | Có checkpoint | Chạy `src.evaluate` | Có Top-1, Top-5, per-class CSV, top 20 cặp nhầm, hình ảnh sai cho cả hai mô hình |
| AC-010 | Có checkpoint ViT | Chạy `src.attention` | Có hình cho ít nhất 12 ảnh, gồm cả đúng và sai |
| AC-011 | Có JSON kết quả | Chạy `src.compare` | Bảng khớp với JSON, có đủ khóa kể cả `macs`, `peak_vram_mb`; số thiếu hiện "chưa có" |

## Cách chạy

| Mục đích | Lệnh | Điều kiện | Trạng thái |
|---|---|---|---|
| Đánh giá | `python -m src.evaluate` | Có checkpoint | Chưa có code |
| Attention | `python -m src.attention --checkpoint outputs/checkpoints/vit_small_seed42_best.pt --split test` | Checkpoint ViT đã chốt, cache test và class_names khớp | Đã chạy CPU 2026-11-20; 12 ảnh, chờ TV1 review |
| So sánh | `python -m src.compare` | Có JSON kết quả | Chưa có code |

## Rủi ro
- Rò rỉ dữ liệu test: đánh giá số cuối và vẽ attention chỉ sau khi chốt cấu hình/checkpoint. Không dùng nhóm ảnh đã chọn cân bằng đúng/sai để báo accuracy hoặc chọn mô hình.
