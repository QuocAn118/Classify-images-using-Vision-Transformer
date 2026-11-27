# Phân loại ảnh Tiny ImageNet bằng Vision Transformer

Đồ án môn Học sâu, đề số 9. Nhóm tự cài ViT, so sánh với một CNN có cùng số tham số và trực quan hóa attention.

> **Trạng thái:** đã có khung repo, dữ liệu, DataLoader (TASK-001 đến 003), ViT ([PR #2](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/2)), CNN ([PR #3](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/3)), vòng lặp train và train thật 50 epoch (TASK-006, 011, TV4, gộp từ nhánh `hoangdang`) và hình attention (TASK-008, [PR #6](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/6)). Validation Top-1: ViT 47,63%, CNN 58,73% ([bằng chứng](outputs/results/task011_training_checks.json)). Đánh giá test, bảng so sánh và demo Gradio (TASK-007, 009, 010, TV5, [PR #11](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/11)). Test Top-1: ViT 48,46%, CNN 59,03% ([ViT](outputs/results/vit_small_seed42.json), [CNN](outputs/results/cnn_baseline_seed42.json), [bảng so sánh](outputs/results/comparison.md)).

## Bài toán

Phân loại ảnh 64x64 vào 200 lớp. Dự án trả lời hai câu hỏi: với cùng số tham số, ViT so với CNN thế nào trên tập dữ liệu nhỏ, và ViT nhìn vào vùng nào của ảnh khi dự đoán.

## Tính năng

- ViT tự cài bằng PyTorch (patch embedding + Transformer encoder).
- ResNet nhỏ có số tham số chênh không quá 5% so với ViT.
- Bảng so sánh Top-1, Top-5, số tham số, FLOPs, thời gian train, tốc độ inference và VRAM (MACs ghi "chưa có").
- Hình CLS attention và attention rollout.
- Demo Gradio: tải ảnh lên, xem Top-5 và ảnh attention.

## Kiến trúc

Xem sơ đồ và thành phần tại [docs/02_architecture.md](docs/02_architecture.md); mỗi thành phần có một file riêng trong `docs/`.

## Cài đặt và chạy

Repo không chứa dữ liệu. Mỗi máy tự tải và tạo cache (DEC-015):

```bash
pip install -r requirements.txt        # máy GPU: cài torch bản CUDA trước
python scripts/prepare_data.py --download
python -m pytest
```

- `prepare_data.py --download` tải Tiny ImageNet từ Stanford (248 MB) vào `data/`, chia train/validation/test và tạo cache khoảng 1,35 GB ở `data/cache/tiny_imagenet_64/`. Trên máy TV1 (CPU, Windows) mất 64 phút.
- Đánh giá test, so sánh và demo: lệnh ở mục dưới.

### Đánh giá, so sánh và demo (TV5)

**Checkpoint:** tải từ [Google Drive](https://drive.google.com/drive/folders/1tt17rM1VGNZwshr4-DTt4OMNHc0IA6BE?usp=drive_link) (không nằm trong Git) và đặt vào `outputs/checkpoints/`. Đối chiếu SHA-256 trước khi dùng:

| File | SHA-256 |
|---|---|
| `vit_small_seed42_best.pt` | `97fbd0daa0e088b4b7d8a9c9adca4f61ba858986f00daa9669c83196a5a7b66b` |
| `cnn_baseline_seed42_best.pt` | `cb2690b3220ad565c4d947a0ba38f18b6653e5447a19050386a8e9b9d659c195` |

Kiểm tra: `certutil -hashfile <file> SHA256` (Windows) hoặc `sha256sum <file>`. Mã của các file `_last` ghi trong [task011_training_checks.json](outputs/results/task011_training_checks.json).

```bash
python -m src.evaluate
python -m scripts.error_analysis
python -m src.compare
python app/demo.py
```

Đánh giá và phân tích lỗi cần cache test. So sánh đọc kết quả trong `outputs/results/`; số chưa đo hiển thị “chưa có”. Demo chỉ cần checkpoint và các thư viện trong `requirements.txt`, không cần tải bộ dữ liệu. Thiếu hoặc hỏng checkpoint sẽ có thông báo hướng dẫn. Ảnh mẫu và thông tin nguồn ở [app/examples/README.md](app/examples/README.md).

### Huấn luyện (TV4)

Môi trường Windows của TV4 dùng `.venv/Scripts/python.exe` thay `python` trong các lệnh bên dưới. Tạo môi trường bằng `python -m venv .venv`, cài PyTorch CUDA theo [hướng dẫn chính thức](https://pytorch.org/get-started/locally/) trước, rồi cài `requirements.txt`. Trên RTX 5060 Laptop của TV4 đã kiểm tra torch 2.11.0+cu128 và torchvision 0.26.0+cu128. Nếu terminal lỗi mã hóa tiếng Việt, đặt `$env:PYTHONUTF8 = "1"` và `$env:PYTHONIOENCODING = "utf-8"` trong PowerShell.

```bash
python -m src.train --config configs/vit_small.yaml --quick --device cpu
python -m src.train --config configs/cnn_baseline.yaml --quick --device cuda
python -m src.train --config configs/vit_small.yaml
python -m src.train --config configs/cnn_baseline.yaml
python -m src.train --config configs/vit_small.yaml --resume outputs/checkpoints/vit_small_seed42_last.pt
```

Quick chạy tối đa 2 epoch × 2 batch mỗi tập, thiếu cache thì cảnh báo và dùng dữ liệu giả. Tên có `_quick` để không ghi đè train thật; giữ batch 64 và kiến trúc mặc định khi đo VRAM. Train thật cần cache cùng `outputs/results/class_names.json`, chạy lần lượt ViT rồi CNN, mặc định 50 epoch, chọn checkpoint bằng validation; không đọc test. Hai lệnh train thật đã chạy đủ 50 epoch cho TASK-011; số liệu và kiểm chứng nằm ở [task011_training_checks.json](outputs/results/task011_training_checks.json), bảng validation và đường cong ở [báo cáo mục 4.2](report/report.md#42-huấn-luyện-đường-cong-học-và-ablation).

Checkpoint best/last ở `outputs/checkpoints/`, CSV ở `outputs/logs/`, hình đường cong ở `outputs/figures/`. Chưa có resume thì chương trình từ chối ghi đè lần chạy cũ. Resume giữ cùng model, seed, batch và lịch số epoch tổng. Chi tiết và bằng chứng: [06_training.md](docs/06_training.md), [task006_training_checks.json](outputs/results/task006_training_checks.json). Dữ liệu và checkpoint không commit; checkpoint best tải ở link Google Drive mục dưới. Trên máy TV4, pytest cần thư mục tạm riêng: `python -m pytest -q -W error --basetemp .git/codex/pytest-local` (thư mục cha `.git/codex/` đã được tạo trong phiên này).

### Kiểm tra ViT (TASK-004)

Không cần tải dữ liệu để chạy test mô hình:

```bash
python -m pytest tests/test_models.py -q -W error
```

Đã chạy trên CPU ngày 2026-11-17: 23 test mô hình pass; toàn bộ repo 48 test pass. ViT mặc định có **6.436.296 tham số**, forward ảnh `(2,3,64,64)` cho logits `(2,200)`; `return_attn=True` trả thêm 8 tensor attention `(2,8,65,65)`. Bằng chứng forward/backward bằng dữ liệu giả: [task004_vit_checks.json](outputs/results/task004_vit_checks.json). Cách tạo mô hình và giải thích luồng xử lý: [docs/05_model.md](docs/05_model.md).

### Trực quan hóa attention (TASK-008)

Đặt checkpoint ViT đã chốt tại `outputs/checkpoints/vit_small_seed42_best.pt` (không commit). Sau khi chuẩn bị cache bằng `prepare_data.py`, chạy:

```bash
python -m src.attention --checkpoint outputs/checkpoints/vit_small_seed42_best.pt --split test --num-images 12 --scan-limit 512 --seed 42 --device cpu
```

CLI lấy kiến trúc, mean/std và tên lớp từ checkpoint, đối chiếu thứ tự nhãn với `outputs/results/class_names.json`; `--expected-sha256` cho phép xác minh file bàn giao, `--cache-dir` đổi nơi đọc cache. Mặc định dùng validation; test chỉ đọc khi chỉ định `--split test` và checkpoint đã chốt.

Đã chạy ngày 2026-11-20: **12 ảnh, 12 lớp, 6 đúng và 6 sai**. Xem [gallery](outputs/figures/attention/vit_small_seed42_test/gallery.png), [manifest từng ảnh](outputs/figures/attention/vit_small_seed42_test/manifest.json) và [bằng chứng](outputs/results/task008_attention_checks.json). Toàn repo **73 test pass**; không đo accuracy từ tập ảnh được chọn cân bằng này. API dùng lại cho demo ở [docs/07_evaluation.md](docs/07_evaluation.md). Chưa kiểm tra CUDA/AMP; TV1 đã chạy lại và gộp TASK-008.

## Tài liệu

| File | Nội dung |
|---|---|
| [Project_description.md](Project_description.md) | Tóm tắt Define, Design, Plan và mục lục `docs/` |
| [docs/](docs/) | Tài liệu theo thành phần: dữ liệu, mô hình, huấn luyện, đánh giá, demo; kèm define, kiến trúc, quyết định, kế hoạch, nhật ký |
| [SPEC_ViT.md](SPEC_ViT.md) | Yêu cầu kỹ thuật chi tiết, nháp mẫu đăng ký |
| [report/report.md](report/report.md) | Báo cáo cuối của nhóm (đang viết): mỗi mục ghi người phụ trách và nội dung bắt buộc; đã có phần dữ liệu và kiến trúc ViT |
| [AGENTS.md](AGENTS.md) | Quy tắc cho người và AI khi làm việc trong repo |
| [AI_Usage.md](AI_Usage.md) | Ghi nhận việc dùng AI |
| [workflow/](workflow/) | Quy trình 14 bước giảng viên yêu cầu |
| [.github/](.github/) | Mẫu Issue và PR, nơi ghi các bước Describe, Review, Test |
