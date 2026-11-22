# Nhật ký làm việc

Ghi ngắn sau mỗi buổi hoặc mốc đáng kể.

## 2026-11-07

- **Đầu việc:** TASK-000 (tài liệu).
- **Kết quả / thay đổi chính:**
  - Phân tích đề và sửa `SPEC_ViT.md` theo đề gốc, thêm phân công, lịch, nháp mẫu đăng ký.
  - Điền `docs/`, viết `README.md`, `AGENTS.md`, `AI_Usage.md`.
  - Chốt train trên máy GPU của một thành viên, Kaggle hoặc Colab là dự phòng.
  - AI đã viết thử TASK-001 trước khi `docs/` hoàn thành, sai thứ tự quy trình. Nhóm quyết định xóa và làm lại sau khi `docs/` được duyệt.
- **Bằng chứng kiểm tra:** Tài liệu chưa được nhóm đọc. Repo chưa có code nên chưa có kết quả chạy.
- **Điều tôi giải thích được về code:** Chưa có code.
- **Điều chưa hiểu / chưa xác minh:** Các giả định trong `../01-define/DEFINE.md`.
- **Bước tiếp theo:** Nhóm đọc và duyệt `docs/`, chốt TV, nộp mẫu đăng ký, rồi mới bắt đầu TASK-001.

## 2026-11-07 (chỉnh sửa theo quyết định nhóm)

- **Đầu việc:** TASK-000 (tài liệu).
- **Kết quả / thay đổi chính:**
  - Quyết định: số chưa đo ghi là "dự đoán"; train 50 epoch và đây là mức sàn; batch 64, lr ViT 2,5e-4 cho cả ViT và CNN; bỏ ViT pretrained; áp dụng nhận xét của senior.
  - File đã sửa: `SPEC_ViT.md`, `docs/01_DEFINE.md`, `docs/02_REQUIREMENTS.md`, `docs/03_DESIGN.md`, `docs/04_BREAKDOWN.md`, `docs/05_TOOLS.md`, `docs/06_VERIFICATION.md`, `docs/07_WORK_LOG.md`, `AGENTS.md`, `AI_Usage.md`.
  - Quyết định thêm: giai đoạn tài liệu làm thẳng trên `main`, từ TASK-001 mỗi người làm nhánh riêng rồi mở PR, TV1 duyệt; thứ tự cắt việc là CNN thứ hai, ablation, 3 seed, Grad-CAM, cuối cùng mới đến đo FLOPs/MACs.
  - Áp dụng 11 điểm rà soát tài liệu. Hợp đồng dùng chung đổi: JSON thêm `macs`, `peak_vram_mb`; checkpoint thêm `scaler`, `class_names`; config thêm `mean`, `std`; tên lần chạy gồm seed; `--quick` dùng dữ liệu giả khi chưa có cache. Cần báo cả nhóm.
- **Bằng chứng kiểm tra:** Chỉ rà soát tài liệu bằng `grep`; chưa có code nên chưa có kết quả chạy.
- **Điều tôi giải thích được về code:** Chưa có code.
- **Điều chưa hiểu / chưa xác minh:** FLOPs/MACs, thời gian train, VRAM, mức Top-1 dự đoán; nội dung tài liệu chưa được nhóm duyệt.
- **Bước tiếp theo:** Nhóm đọc và duyệt `docs/`, chốt TV, nộp mẫu đăng ký, rồi mới bắt đầu TASK-001.

## 2026-11-14

- **Đầu việc:** TASK-000 (tài liệu).
- **Kết quả / thay đổi chính:**
  - Nhóm xóa `.agents/docs/` (bộ mẫu cũ) và đổi tên `.agents/` thành `workflow/`.
  - Thử chia `docs/` theo 14 bước của `workflow/` nhưng nhiều file rỗng; nhóm chọn chia theo thành phần (DEC-013).
  - `docs/` mới: `01_define.md`, `02_architecture.md`, `09_decisions.md`, `03_plan.md`, `04_data.md`, `05_model.md`, `06_training.md`, `07_evaluation.md`, `08_demo.md`, `10_work_log.md`. Nội dung cũ được chuyển sang, không thêm yêu cầu mới. FR và AC chuyển về file thành phần; hợp đồng ghi ở file của bên tạo ra nó.
  - `Project_description.md` thành bản tóm tắt Define, Design, Plan.
  - Trạng thái đầu việc chuyển lên GitHub Issues và Projects (chưa tạo). Thêm mẫu PR, mẫu Issue "Đầu việc" và "Lỗi" trong `.github/`.
  - Sửa `AGENTS.md`, `README.md` theo cấu trúc mới.
- **Bằng chứng kiểm tra:** Script kiểm tra link tương đối và đối chiếu mã FR, AC, DEC, TASK giữa bản cũ và bản mới.
- **Điều tôi giải thích được về code:** Chưa có code.
- **Điều chưa hiểu / chưa xác minh:** Nội dung tài liệu chưa được nhóm duyệt; giảng viên chưa xác nhận cách nộp bằng chứng trên Issue/PR.
- **Bước tiếp theo:** Tạo Issue và bảng Projects; hỏi giảng viên về cách nộp bằng chứng; nhóm duyệt `docs/`, chốt TV, nộp mẫu đăng ký.

## 2026-11-15

- **Đầu việc:** TASK-000 (tài liệu).
- **Kết quả / thay đổi chính:** Đánh số file `docs/` theo thứ tự đọc. Nhóm duyệt `docs/`; TASK-000 hoàn thành. Từ đây được bắt đầu code.
- **Bằng chứng kiểm tra:** Nhóm xác nhận duyệt (người dùng báo lại). Script kiểm tra link: 0 link hỏng.
- **Điều tôi giải thích được về code:** Chưa có code.
- **Điều chưa hiểu / chưa xác minh:** Giảng viên chưa xác nhận cách nộp bằng chứng trên Issue/PR. Các mốc M0 đến M3 trong `03_plan.md` đã quá hạn, cần lập lại lịch.
- **Cập nhật:** Giảng viên gia hạn nộp đến 25/11. Lập lại lịch trong `03_plan.md` và mục 20 spec: mục tiêu nộp 24/11, dừng thí nghiệm 21/11, 25/11 dự phòng.
- **Cập nhật:** Người dùng xác nhận mình là TV1 và đã nộp mẫu đăng ký; TASK-014 hoàn thành.
- **Cập nhật:** Đổi tên `AGENT_SPEC_ViT_TinyImageNet.md` thành `SPEC_ViT.md`, sửa tiêu đề cho tự nhiên hơn. TV1 làm mọi đầu việc của mình thẳng trên `main` (DEC-014); không tạo Issue cho đầu việc của TV1.
- **Bước tiếp theo:** Chốt TV2-TV5, TV4 tải thử dữ liệu, tạo Issue, bắt đầu TASK-001.

## 2026-11-15 (TASK-001)

- **Đầu việc:** TASK-001, khung repo và tiện ích dùng chung (TV1, thẳng trên `main`).
- **Kết quả / thay đổi chính:**
  - `src/utils.py`: `load_config` (báo tất cả khóa thiếu trong một lần, AC-013), `make_run_name`, `set_seed`, `count_params`, `atomic_save` (ghi file tạm rồi `os.replace`, lỗi thì xóa file tạm và giữ file cũ, DEC-005).
  - `configs/vit_small.yaml`, `configs/cnn_baseline.yaml` theo spec; phần `data`, `train`, `seed` giống hệt nhau và có test giữ điều này.
  - `.gitignore`, `requirements.txt`, `pytest.ini`, `tests/test_utils.py`.
- **Bằng chứng kiểm tra:**
  - Viết test trước: `python -m pytest -q` → 12 failed (hàm chưa viết). Sau khi viết code: 12 passed.
  - Cố ý làm hỏng code: bỏ bước xóa file tạm → test `keeps_old_file` fail; bỏ khóa `data.mean` khỏi danh sách bắt buộc → test `missing_key` fail. Khôi phục: 12 passed.
  - `git check-ignore` từng đường dẫn: chặn `data/`, checkpoint, `*.pt`, `kaggle.json`, `__pycache__`; không chặn `outputs/logs`, `outputs/results`, `src/`, `configs/`, `workflow/`.
  - Môi trường: Windows 10, Python 3.13.9, torch 2.9.1+cpu, pyyaml 6.0.3, pytest 8.4.2.
- **Điều tôi giải thích được về code:** TV1 đã đọc `src/utils.py` ngày 2026-11-16 và đồng ý đưa lên `main`.
- **Điều chưa hiểu / chưa xác minh:** `atomic_save` chưa thử khi mất điện thật; `os.replace` chỉ nguyên tử khi file tạm và file đích cùng ổ đĩa (đang đảm bảo vì tạo cùng thư mục). Chưa cài thử `requirements.txt` trên máy sạch và máy GPU.
- **Bước tiếp theo:** TV1 làm TASK-002; TV2 bắt đầu TASK-004 trên nhánh riêng.

## 2026-11-16 (TASK-002)

- **Đầu việc:** TASK-002, chuẩn bị dữ liệu, chia tập, xuất mảng cache (TV1, thẳng trên `main`).
- **Kết quả / thay đổi chính:**
  - `scripts/prepare_data.py`: `--download` tải zip từ Stanford (trang Kaggle cần lời mời, DEC-015); đọc nhãn val từ `val_annotations.txt`; kiểm tra số lượng; chia train gốc 90/10 phân tầng seed 42; xuất cache `.npy` (ghi file tạm rồi đổi tên); `class_names.json`, `dataset_stats.json`, `samples.png`.
  - Thêm khóa bắt buộc `data.cache_dir` vào cả hai config và `REQUIRED_KEYS`; thêm `pillow`, `matplotlib` vào `requirements.txt`.
- **Bằng chứng kiểm tra:**
  - Viết test trước: 6 test mới fail (hàm chưa viết), sau khi viết code toàn bộ 18 passed.
  - Cố ý làm hỏng code: bỏ sắp xếp mã lớp → 2 test fail; chia không theo lớp → 2 test fail. Khôi phục: 18 passed.
  - Chạy thật trên máy TV1: "200 lớp, 100000 ảnh train gốc, 10000 ảnh val gốc"; `{"train": 90000, "val": 10000, "test": 10000}`, cache 1.35 GB; đếm nhãn trong cache: mỗi lớp 450 train / 50 val / 50 test. Thời gian 64 phút.
  - Ảnh mẫu lần đầu chỉ có một lớp (lấy 25 ảnh đầu) và đường dẫn trong stats dùng `\`; đã sửa (lấy ngẫu nhiên, đường dẫn dạng `/`, có test), tạo lại hai file này từ cache.
- **Điều tôi giải thích được về code:** TV1 đã đọc `scripts/prepare_data.py` ngày 2026-11-17 và đồng ý đưa lên `main`.
- **Điều chưa hiểu / chưa xác minh:** Chưa chạy lại toàn bộ trên dữ liệu thật sau lần sửa cuối (chỉ tạo lại ảnh mẫu và stats); chưa thử `--download` trên Linux/máy GPU; chưa có test cho trường hợp ghi `.npy` bị lỗi giữa chừng. Vì sao chạy mất 64 phút chưa đo (nghi do đọc 110.000 file nhỏ trên Windows).
- **Bước tiếp theo:** TV1 làm TASK-003; TV2 làm TASK-004 trên nhánh riêng.

## 2026-11-17 (TASK-003)

- **Đầu việc:** TASK-003, DataLoader đọc mảng cache và augmentation (TV1, thẳng trên `main`).
- **Kết quả / thay đổi chính:**
  - `src/data.py`: `build_loader(cfg, split)` và `CachedDataset`; mở cache bằng mmap lười, không pickle cả mảng sang worker (Windows tạo worker bằng spawn); train: RandomCrop padding 4, lật ngang, RandAugment, RandomErasing theo config; val/test: chỉ chuẩn hóa.
  - Hợp đồng ghi trong `docs/04_data.md`. Sửa các chỗ còn ghi Kaggle trong `SPEC_ViT.md`; thêm hướng dẫn chạy vào `README.md`.
- **Bằng chứng kiểm tra:**
  - Viết test trước: 7 test mới fail (chưa có code); sau khi viết code: 25 passed (coi cảnh báo là lỗi).
  - Cố ý làm hỏng code: bỏ `__getstate__` → test pickle fail; val bỏ Normalize → test val fail; train không bỏ batch lẻ → test option fail. Khôi phục: 25 passed.
  - Cache thật, `configs/vit_small.yaml`, 4 worker, CPU: batch `(64, 3, 64, 64)` float32; 1406 batch train/epoch, 157 batch val; train khoảng 825 ảnh/giây, val khoảng 3.223 ảnh/giây (100 batch, một lần đo).
- **Điều tôi giải thích được về code:** TV1 đã đọc `src/data.py` ngày 2026-11-17 và đồng ý đưa lên `main`.
- **Điều chưa hiểu / chưa xác minh:** Chưa đo trên máy GPU; chưa biết GPU có phải chờ DataLoader không.
- **Bước tiếp theo:** TV2 làm TASK-004, TV3 làm TASK-005, TV4 làm TASK-006 trên nhánh riêng.

## 2026-11-17 (hợp đồng tạo mô hình)

- **Đầu việc:** chốt hợp đồng dùng chung `build_model(cfg)` trong `docs/05_model.md` trước khi TV2, TV3, TV4 bắt đầu.
- **Kết quả / thay đổi chính:** thêm `build_model(cfg)` (chọn theo `model.name`) vào hợp đồng mô hình; TV1 chốt làm lần lượt TASK-004 → 005 → 006, không cắt việc, giữ các mốc hiện tại.
- **Bằng chứng kiểm tra:** chỉ sửa tài liệu, chưa có code.
- **Điều chưa hiểu / chưa xác minh:** TV2, TV3, TV4 chưa xác nhận đã đọc hợp đồng.
- **Bước tiếp theo:** TV1 nhắn TV2 bắt đầu TASK-004 trên nhánh riêng.

## 2026-11-17 (Codex đọc dự án)

- **Đầu việc:** Đọc và nắm hiện trạng theo yêu cầu người dùng; chưa bắt đầu đầu việc code mới.
- **Kết quả / thay đổi chính:** Đọc quy tắc repo, spec, tài liệu thành phần, kế hoạch, nhật ký, config, mã nguồn và test hiện có. Code đang có TASK-001 đến TASK-003; đầu việc tiếp theo theo kế hoạch là TASK-004 (ViT và `build_model(cfg)`).
- **Bằng chứng kiểm tra:** `python -m pytest -q -W error` → 25 passed in 33.51s. Máy hiện tại không có thư mục `data/cache/tiny_imagenet_64/`; số lượng dữ liệu trong `outputs/results/dataset_stats.json` là kết quả đã lưu, chưa kiểm chứng lại trên dữ liệu thật trong buổi này.
- **Điều chưa hiểu / chưa xác minh:** Chưa kiểm tra trạng thái GitHub Issues/Projects trực tiếp (`gh` chưa cài). `Project_description.md` còn ghi TASK-001 là bước tiếp theo; mục hiện trạng trong `docs/02_architecture.md` chưa cập nhật TASK-002, 003. Chưa sửa các nội dung này trong buổi đọc.
- **Bước tiếp theo:** Khi được giao triển khai, thực hiện một đầu việc theo `docs/03_plan.md` và hợp đồng tương ứng.

## 2026-11-17 (TASK-004, TV2)

- **Đầu việc:** TASK-004, ViT tự cài và test. Người dùng xác nhận mình là TV2; làm trên nhánh riêng, không áp dụng ngoại lệ TV1 làm thẳng trên `main`.
- **Chuẩn bị / Describe:** Đọc lần lượt file gốc trước rồi `docs/` và workflow. Giữ các ghi chú chưa commit của buổi đọc trước bằng stash, `git pull --ff-only origin main` → Already up to date (`b29de54`), tạo `tv2/task-004-vit` rồi khôi phục ghi chú. Tạo [Issue #1](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/issues/1) theo mẫu trước khi viết code.
- **Kết quả / thay đổi chính:** `src/models/vit.py` có patch embedding, CLS/positional embedding học được, encoder Pre-LN, MLP GELU, DropPath tăng theo độ sâu, SDPA và nhánh attention tường minh trả weights trước dropout. `src/models/__init__.py` tạo ViT qua `build_model(cfg)`; chưa có CNN (TASK-005). Thêm `tests/test_models.py`, bằng chứng JSON, cập nhật `docs/05_model.md`, README và AI_Usage. Không đổi hợp đồng hay thêm dependency.
- **Bằng chứng kiểm tra:**
  - Viết test trước: `python -m pytest tests/test_models.py -q -W error` → lỗi collection do `src.models` chưa có. Sau khi triển khai: 23 passed.
  - `python -m pytest -q -W error` → 48 passed (gồm 25 test cũ).
  - Smoke test cấu hình mặc định bằng dữ liệu giả: `(2,3,64,64)` → `(2,200)`, 8 attention `(2,8,65,65)`, 6.436.296 tham số; sai khác logits tối đa 7,15e-7, tổng hàng attention sai tối đa 2,38e-7; backward cho gradient hữu hạn ở mọi tham số, một bước AdamW cập nhật head. Kết quả lưu [task004_vit_checks.json](../outputs/results/task004_vit_checks.json).
  - Môi trường thực tế: Windows, Python 3.12.10, torch 2.15.0+cpu; không có CUDA. `git diff --check` không báo lỗi.
- **Giải thích / Review:** Luồng patch → CLS + positional embedding → 8 encoder → LayerNorm → head ghi trong `docs/05_model.md`. Tự đối chiếu AC-004/005, config và factory; không đọc dữ liệu test thật, không lưu checkpoint. TV1 chưa review, không tự đánh dấu Hoàn thành.
- **Điều chưa xác minh / giới hạn:** Chưa đo GPU, AMP hoặc VRAM; chưa train và chưa có accuracy. `--quick` thuộc TASK-006. GitHub xác thực bằng `BinhNg1208`, hiện chưa có quyền push vào repo gốc; token thiếu quyền Projects (`read:project`), nên chưa cập nhật bảng Projects. Trạng thái/bằng chứng sẽ ghi ở Issue; bản mô tả PR chuẩn bị tại `.git/codex/TASK-004_PR.md`. Chưa commit/push vì chưa được yêu cầu.
- **Bước tiếp theo:** TV2 đọc và giải thích được code; commit/push khi được yêu cầu, mở PR gắn Issue #1 để TV1 review. Chỉ sau khi gộp TASK-004 mới chuyển TASK-005 theo kế hoạch.

## 2026-11-17 (TASK-004, nhánh thanhbinh)

- **Đầu việc:** Chốt thay đổi TASK-004 trên nhánh `thanhbinh` theo yêu cầu người dùng; từ đây các thay đổi của TV2 trong phiên này được commit trên nhánh này.
- **Kết quả / thay đổi chính:** Tạo và chuyển sang `thanhbinh` bằng `git switch -c thanhbinh`, giữ toàn bộ thay đổi TASK-004 và ghi chú buổi đọc. Cập nhật tên nhánh hiện tại trong README, tài liệu mô hình và AI_Usage. Commit dự kiến: `TASK-004: implement ViT with attention outputs and 23 model tests`.
- **Bằng chứng kiểm tra:** Code không đổi so với lần kiểm tra 48 test pass và smoke test trước đó; chỉ đổi ghi nhận nhánh/tài liệu. Kiểm tra diff và staged diff trước commit, đối chiếu ref `main` sau commit để bảo đảm không thay đổi.
- **Giới hạn / bước tiếp theo:** Chưa push hoặc mở PR; TASK-004 vẫn chờ TV1 review. Quyền GitHub Projects và quyền push vào repo gốc còn thiếu như bản ghi trước.

## 2026-11-17 (TASK-004, push nhánh thanhbinh và mở PR)

- **Đầu việc:** Bàn giao TASK-004 để TV1 review theo yêu cầu tiếp tục của người dùng; chỉ commit/push trên `thanhbinh`, không merge vào `main`.
- **Kết quả / thay đổi chính:** `git fetch origin main` xác nhận nhánh đã chứa main mới nhất (`b29de54`). Tài khoản `BinhNg1208` chưa có quyền push repo gốc, nên tạo fork `BinhNg1208/Classify-images-using-Vision-Transformer`, thêm remote `fork` và `git push --set-upstream fork thanhbinh:thanhbinh`. Mở [PR #2](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/2), nguồn `BinhNg1208:thanhbinh`, đích `QuocAn118:main`, gắn `Closes #1`; PR đang mở và chưa merge. Cập nhật README, tài liệu mô hình và AI_Usage với link PR.
- **Bằng chứng kiểm tra:** `git merge-base --is-ancestor origin/main HEAD` và `git diff origin/main...HEAD --check` đều đạt; audit file tracked không có dữ liệu, checkpoint hay `kaggle.json`. Code vẫn ở commit `73ac662`, đã có 48 test pass và bằng chứng smoke test từ buổi triển khai; buổi bàn giao chỉ đổi tài liệu nên không chạy lại test. Nhánh `thanhbinh` theo dõi `fork/thanhbinh`; local `main` giữ nguyên tại `b29de54`.
- **Giới hạn:** Yêu cầu reviewer `QuocAn118` qua API chưa thành công (HTTP 404), nên chưa có reviewer được gán tự động. Token vẫn thiếu quyền GitHub Projects; chưa cập nhật được bảng. Không tự đóng Issue hoặc đánh dấu TASK-004 Hoàn thành; chưa chạy GPU/AMP/VRAM.
- **Bước tiếp theo:** TV1 đọc PR và quyết định merge. TASK-008 chưa bắt đầu vì TASK-006 và checkpoint chưa có; không mở rộng sang đầu việc khác trong buổi bàn giao.

## 2026-11-17 (TASK-004, phần báo cáo TV2)

- **Đầu việc:** Bổ sung báo cáo theo yêu cầu người dùng, trong bước Documentation của TASK-004 trên `thanhbinh`; không triển khai đầu việc code mới.
- **Describe / kết quả:** Bổ sung phạm vi báo cáo vào [Issue #1](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/issues/1) trước khi viết. Repo chưa có báo cáo, nên tạo `report/report.md` với khung 10 mục theo spec; viết phần ViT ở mục 3 (sơ đồ, config, patch/CLS/positional embedding, Pre-LN, hai nhánh attention, DropPath, head, khởi tạo và factory), kiểm chứng tại mục 4.1 và trạng thái/phương án attention ở mục 6. Các phần còn lại chờ thành viên phụ trách, chỉ số chưa đo và hình chưa sinh ghi "chưa có". Thêm link báo cáo trong README và ghi nhận AI.
- **Nguồn và kiểm chứng:** Đối chiếu mô tả với `src/models/vit.py`, factory, YAML, `outputs/results/task004_vit_checks.json` và nhật ký test; không thêm số liệu huấn luyện. Kiểm tra nguồn tham khảo tại arXiv:2010.11929 và ACL Anthology:2020.acl-main.385. Kiểm tra UTF-8, link tương đối, cấu trúc mục, công thức và whitespace; chỉ sửa Markdown nên không chạy lại unit test. Bằng chứng 48 test pass vẫn thuộc buổi triển khai trước.
- **Giới hạn / bước tiếp theo:** Báo cáo là bản nháp, chưa có kết quả huấn luyện hoặc hình attention; chưa đánh dấu TASK-008 hay báo cáo cuối hoàn thành. Cập nhật commit lên `fork/thanhbinh` để PR #2 nhận phần báo cáo, chờ TV1 review; không push hoặc merge vào main. Quyền GitHub Projects vẫn thiếu như buổi trước.

## 2026-11-17 (TV1 review và gộp PR #2, khung báo cáo)

- **Đầu việc:** review TASK-004 (TV2), gộp vào `main`, cập nhật trạng thái; hoàn thiện khung `report/report.md` cho cả nhóm.
- **Kết quả / thay đổi chính:**
  - Gộp PR #2 bằng `git merge --no-ff`, giữ 3 commit tác giả Thanh Binh.
  - Sửa các dòng "chờ review" (README, `05_model.md`, `AI_Usage.md`) và trạng thái cũ trong `Project_description.md`, `02_architecture.md`, `03_plan.md`.
  - TASK-008: code và test làm được ngay với mô hình trọng số ngẫu nhiên; chỉ hình thật cần checkpoint.
  - Báo cáo: giữ phần ViT của TV2; thêm bảng phân công theo mục 19 spec, nội dung bắt buộc của từng mục theo mục 15, mục mã nguồn, tài liệu tham khảo còn thiếu; viết mục 2 (Dữ liệu) từ `dataset_stats.json`.
- **Bằng chứng kiểm tra:** chạy nhánh PR trong worktree tạm: `python -m pytest -q -W error` → 48 passed; sau khi gộp trên `main`: 48 passed. Không có file dữ liệu/checkpoint trong PR; `git diff --check` sạch. ViT chạy được dưới autocast bf16 ở cả hai nhánh attention.
- **Điều chưa xác minh:** chưa chạy ViT trên CUDA/AMP fp16 và chưa đo VRAM (TASK-006). Issue #1 có thể phải đóng tay vì PR được gộp bằng git trên máy.
- **Bước tiếp theo:** TV3 làm TASK-005; TV2 làm TASK-008.

## 2026-11-18

- **Đầu việc:** TASK-005 (CNN và `match_param_count`).
- **Kết quả / thay đổi chính:**
  - Thêm `src/models/cnn.py` với ResNet nhỏ làm baseline so sánh với ViT.
  - Thêm `match_param_count` để tìm cấu hình CNN có số tham số gần với ViT-small.
  - Cấu hình được chọn: `widths=(64, 128, 256, 512)`, `blocks=(1, 2, 2, 1)`, `stem_stride=2`.
  - CNN có **6.476.808 tham số**, so với ViT **6.436.296 tham số**, chênh lệch khoảng **0,63%**, nằm trong yêu cầu không quá 5%.
  - `build_model(cfg)` đã tạo được `resnet_small` từ `configs/cnn_baseline.yaml`.
  - Bổ sung kiểm tra cho CNN và factory; toàn bộ test hiện tại đều pass.

- **Bằng chứng kiểm tra:**
  - `python -c "from src.models.cnn import match_param_count; c,n=match_param_count(6436296); print(c); print(f'{n:,} params')"` → `ResNetConfig(widths=(64, 128, 256, 512), blocks=(1, 2, 2, 1), stem_stride=2)`; `6,476,808 params`.
  - `python -c "from src.models import build_model; from src.utils import load_config,count_params; c=load_config('configs/cnn_baseline.yaml'); m=build_model(c); print(f'{count_params(m):,} params')"` → `6,476,808 params`.
  - `python -m pytest tests/test_models.py -q -W error` → **24 passed**.
  - `python -m pytest -q -W error` → **49 passed**.
  - `python .\measure_flops.py` → **809.050.112 FLOPs**.
  - `python .\measure_vit_flops.py` → **824.283.136 FLOPs**.

- **Điều tôi giải thích được về code:**
  - `match_param_count` tìm cấu hình ResNet có số tham số gần mục tiêu của ViT thay vì cố định thủ công một cấu hình.
  - CNN dùng cùng cấu hình data và training với ViT thông qua `configs/cnn_baseline.yaml`.
  - `build_model` là điểm tạo model chung; bên ngoài không cần import trực tiếp lớp CNN.
  - Với cấu hình đã chọn, CNN có số tham số gần ViT và FLOPs thấp hơn ViT trong phép đo hiện tại.

- **Điều chưa hiểu / chưa xác minh:**
  - Chưa chạy huấn luyện thật nên chưa có accuracy/loss của CNN để so sánh với ViT.
  - Chưa đo FLOPs trên GPU hoặc trong điều kiện huấn luyện thực tế.
  - Grad-CAM chưa thực hiện.

- **Bước tiếp theo:**
  - Bàn giao phần model cho TASK-006 để tích hợp vào vòng lặp train.
  - Nếu còn trong phạm vi công việc của TV3, thực hiện Grad-CAM hoặc các phép đo bổ sung theo thứ tự cắt việc của nhóm.

## 2026-11-19

- **Đầu việc:** TASK-005, tiếp thu review của TV1.
- **Kết quả / thay đổi chính:**
  - Tối ưu `match_param_count()` bằng `torch.device("meta")` để tạo mô hình phục vụ đếm tham số mà không cấp phát bộ nhớ cho trọng số.
  - Sử dụng `count_params` từ `src.utils`, loại bỏ hàm đếm tham số trùng lặp trong `src/models/cnn.py`.
- **Bằng chứng kiểm tra:**
  - `python -m pytest tests/test_models.py -q -W error` → **27 passed in 30.47s**.
  - `python -m pytest -q -W error` → **52 passed in 36.82s**.
  - Kết quả đo lưu tại `outputs/results/task005_cnn_checks.json`, sử dụng `torch.utils.flop_counter.FlopCounterMode`, chế độ `eval`, batch size 1, input `(1, 3, 64, 64)`:
    - ResNet-small: **6.476.808 parameters**, **809.050.112 FLOPs**.
    - ViT-small: **6.436.296 parameters**, **824.283.136 FLOPs**.
    - Sai số tương đối số tham số: **0,629%**; ResNet-small có FLOPs thấp hơn ViT-small khoảng **1,848%**.
- **Điều tôi giải thích được về code:** `meta device` cho phép tạo cấu trúc mô hình và đếm số phần tử tham số mà không cấp phát tensor trọng số thực.
- **Điều chưa hiểu / chưa xác minh:** Chưa huấn luyện CNN để so sánh accuracy với ViT; chưa thực hiện Grad-CAM.
- **Bước tiếp theo:** Hoàn thiện các chỉnh sửa theo review TV1, cập nhật PR #3 và bàn giao.

## 2026-11-19 (review và gộp PR #3)

- **Đầu việc:** TV1 review TASK-005 (TV3) qua hai vòng, gộp PR #3 vào `main`.
- **Kết quả / thay đổi chính:** vòng 1: `build_model` chạy `match_param_count` mỗi lần tạo CNN (khoảng 52 giây) và hardcode số tham số ViT; TV3 chuyển cấu hình vào `configs/cnn_baseline.yaml`. Vòng 2: hai test `match_param_count` mỗi test khoảng 52 giây; TV3 dựng mô hình trên `torch.device("meta")`. Gộp bằng merge commit để giữ commit của TV3; TV1 sửa thêm dòng trống trong `cnn.py` và nhật ký.
- **Bằng chứng kiểm tra:** máy TV1 (CPU): `python -m pytest -q -W error` → 52 passed trong 1 phút 30 giây; `build_model` CNN 0,6 giây, 6.476.808 tham số (chênh 0,63% so với ViT 6.436.296); FLOPs mỗi ảnh đo lại bằng `FlopCounterMode` khớp `task005_cnn_checks.json` (CNN 809.050.112, ViT 824.283.136).
- **Điều chưa xác minh:** chưa chạy CNN trên CUDA, chưa đo VRAM (TASK-006).
- **Bước tiếp theo:** TV4 làm TASK-006; TV2 làm TASK-008.

## 2026-11-19 (Codex đọc tài liệu)

- **Đầu việc:** Đọc tài liệu theo yêu cầu người dùng, chưa bắt đầu đầu việc triển khai mới.
- **Kết quả:** Đọc README, Project_description, spec, toàn bộ `docs/`, AI_Usage và bản nháp báo cáo. Nắm phạm vi, phân công, hợp đồng và tiến độ được ghi nhận: TASK-001 đến 004 đã xong; tiếp theo TASK-005 → TASK-006, song song TASK-008.
- **Đối chiếu tài liệu:** Spec mục 6 còn ghi số tham số ViT chưa xác minh bằng code; bảng lệnh trong `02_architecture.md` còn ghi 25 test, trong khi nhật ký review TASK-004 ghi 48 test pass. Chưa sửa các nội dung này trong buổi đọc.
- **Giới hạn:** Chưa đối chiếu code, chạy lại test hoặc kiểm tra GitHub Issues/Projects; các kết quả và trạng thái trên là thông tin đã ghi trong tài liệu. Chỉ cập nhật nhật ký và ghi nhận AI, không commit/push.
- **Bước tiếp theo:** Chờ đầu việc cụ thể từ người dùng; giữ phạm vi một đầu việc theo kế hoạch.

## 2026-11-19 (đồng bộ nhánh hoangdang và đọc lại docs)

- **Đầu việc:** Kiểm tra các nhánh, gộp phần còn thiếu vào nhánh hiện tại và đọc lại tài liệu theo yêu cầu người dùng; chưa triển khai đầu việc code mới.
- **Kết quả:** `git fetch --all --prune`; `hoangdang` được fast-forward từ `dc2b84a` lên `59f57c8` (6 commit), bằng `origin/main`. `origin/xbao` (`aff5e82`, TASK-005) đã nằm trong main. Kiểm tra fork `BinhNg1208:thanhbinh` (`107e504`) và refs PR #2/#3 bằng `git ls-remote`: đều là tổ tiên của HEAD; không còn nhánh origin nào chưa gộp vào hoangdang. Local main giữ nguyên.
- **Giữ thay đổi có sẵn:** Sao lưu hai file trong `.git/codex/branch-sync-20261119-211257/`, tạm stash rồi khôi phục; giải quyết xung đột AI_Usage và nhật ký bằng cách giữ cả nội dung mới từ main lẫn toàn bộ ghi chú buổi đọc trước. Không tạo commit mới hoặc push.
- **Bằng chứng kiểm tra:** `git merge-base --is-ancestor` đạt với xbao, thanhbinh và origin/main; `git branch -r --no-merged HEAD` không có kết quả; không còn file unmerged; `git diff --check` đạt. `python -m pytest -q -W error` dừng khi thu thập test: 4 lỗi `ModuleNotFoundError: No module named 'torch'` trên Python 3.12.10 hiện tại. Số 52 test pass trong docs là bằng chứng lịch sử của lần review TASK-005, không phải kết quả chạy lại buổi này.
- **Đọc lại tài liệu:** TASK-001 đến TASK-005 đã được ghi nhận hoàn thành; tiếp theo TASK-006 (TV4, train) và TASK-008 (TV2, code attention với trọng số ngẫu nhiên); hình attention thật cần TASK-011. Chưa có vòng lặp train, checkpoint đã huấn luyện, đánh giá hay demo; không bắt đầu các phần này trong buổi đồng bộ.
- **Nội dung chưa đồng bộ phát hiện khi đọc:** Project_description còn coi TASK-005 là việc tiếp theo và số tham số là tính tay; docs/02_architecture còn ghi chưa có CNN, danh sách khóa bắt buộc thiếu data.cache_dir; docs/03_plan còn ghi chưa có Issue dù đã dẫn Issue #1; đầu báo cáo và bảng mã nguồn mục 8 chưa ghi nhận CNN; SPEC_ViT mục 6 còn ghi số tham số chưa xác minh bằng code; ghi nhận AI của TASK-005 còn ghi chờ review cuối. Chỉ ghi nhận trong buổi đọc, chưa sửa các tài liệu này.
- **Giới hạn:** GitHub CLI chưa đăng nhập; REST API công khai trả lỗi hết hạn mức. Chưa kiểm tra/cập nhật được Issues, reviews hay GitHub Projects trực tiếp; kết luận gộp nhánh dựa trên lịch sử Git và refs công khai. Chưa cài thêm dependency hoặc chạy GPU/train.
- **Bước tiếp theo:** Dùng môi trường có các dependency trong requirements.txt để chạy lại test; nhóm tiếp tục đúng phân công TASK-006 và TASK-008.

## 2026-11-19 (TV4, TASK-006 và bắt đầu TASK-011)

- **Người thực hiện / phạm vi:** Người dùng xác nhận TV4 (Hđang) và giao hoàn thiện phần huấn luyện trên `hoangdang`; giữ nguyên các ghi chú chưa commit của buổi trước. Không làm phần đánh giá/attention/demo của TV khác.
- **Describe:** AGENTS yêu cầu Issue trước code. GitHub CLI chưa đăng nhập, REST hết hạn mức; Computer Use bị dừng vì không xác định được URL Chrome để kiểm tra chính sách. Người dùng chọn lưu mô tả trong repo rồi triển khai: `docs/tasks/TASK-006.md`, sau khi kiểm chứng TASK-006 thì mô tả tiếp TASK-011 riêng. Chưa có Issue/PR/Projects mới trên GitHub.
- **TASK-006:** Thêm `src/train.py`: dùng loader/model/utils sẵn có; AdamW chia nhóm weight decay, warmup/cosine theo iteration, Mixup/CutMix, nhãn mềm/smoothing, AMP và clipping, chọn best trên validation. Quick riêng tên, giữ kiến trúc/batch, fallback dữ liệu giả có cảnh báo. Resume giữ lịch/config, optimizer/scaler/RNG/lịch sử; lưu nguyên tử, phục hồi cả best và CSV; chặn ghi đè khi chưa có resume.
- **Bằng chứng:** `.venv/Scripts/python.exe -m pytest -q -W error --basetemp .git/codex/pytest-task006-final --tb=short --junitxml=.git/codex/task006_pytest.xml` → 72 passed (20 test train). Mặc định pytest không chạy được do Access denied ở thư mục tạm chung, dùng thư mục riêng trong .git; không đổi quyền hệ thống. `pip check` đạt. Quick mặc định ViT/CNN trên CPU (seed 142) và CUDA (seed 42) đều chạy 2 epoch × 2 batch train/val; input giả; nạp lại checkpoint weights_only, model logits hữu hạn và best khớp CSV. CUDA peak allocated: ViT 498,97 MB; CNN 311,35 MB. Nguồn: `outputs/results/task006_training_checks.json`.
- **Review / giải thích:** Train chỉ gọi split train/val; test tích hợp không tạo cache test. Resume thử ngắt sau epoch 6/8, warmup 5, có Mixup/CutMix; so sánh learning rate từng bước ngưỡng 1e-8 và loss với chạy liên tục; phục hồi log/best sai, thử chuyển checkpoint best sang thư mục mới và lỗi ghi CSV. Khóa checkpoint bắt buộc giữ nguyên; trainer thêm lịch sử/RNG và snapshot best để phục hồi, đã ghi rõ ở docs/06_training.md cho bên dùng. Người dùng/TV1 chưa xác nhận đọc code.
- **Môi trường:** Windows, Python 3.12.10, torch 2.11.0+cu128, torchvision 0.26.0+cu128 trong .venv; RTX 5060 Laptop 8GB, driver 582.05 (đã chạy phép toán CUDA). Cài từ kho chính thức PyTorch; không đổi dependency của project. Terminal có đường dẫn tiếng Việt cần PYTHONUTF8/PYTHONIOENCODING=utf-8.
- **TASK-011:** Chạy prepare_data sẵn có với output thống kê/ảnh mẫu trong `.git/codex/task011_data/` để giữ nguyên artifact dữ liệu của TV1. Thực tế đủ 200 lớp, 100.000 train gốc, 10.000 val gốc; cache 90.000 train / 10.000 validation / 10.000 test, 1,35 GB. Thứ tự class_names tạo lại trùng file tracked. Bắt đầu `python -m src.train --config configs/vit_small.yaml --device cuda`, lịch 50 epoch; chưa ghi kết quả cuối khi đang chạy. CNN chạy sau trên cùng GPU. Trainer không đọc test.
- **Tài liệu:** Cập nhật README, Project_description, docs/02, docs/03, docs/06, AI_Usage và phần TV4 (3.3, 4.2) trong báo cáo. Không thêm số test accuracy hoặc accuracy giả; số quick chỉ dùng kiểm chứng pipeline.
- **Giới hạn / trạng thái:** TASK-006 đã triển khai và kiểm thử, chờ TV1 review; chưa đánh dấu Hoàn thành. Chưa có số train cuối hoặc link checkpoint chia sẻ; chưa mô phỏng mất điện vật lý hay GPU 6GB khác. Dữ liệu, .venv, checkpoint được gitignore; không commit/push.
- **Bước tiếp theo:** Theo dõi đủ 50 epoch ViT rồi CNN, kiểm tra checkpoint/log, cập nhật JSON và báo cáo từ file kết quả; TV1 review, đưa Issue/PR lên GitHub khi có quyền.

## 2026-11-19 (TV4, hoàn tất chạy và kiểm chứng TASK-011)

- **Kết quả:** ViT và CNN chạy lần lượt đủ 50 epoch, seed 42, batch 64 trên cùng RTX 5060 Laptop; giữ nguyên hai YAML, cùng data/train. ViT best epoch 50: validation Top-1 47,63%, Top-5 71,77%; CNN best epoch 50: 58,73% / 81,03%. Đây là validation, chưa có test cuối.
- **Hiệu năng:** ViT trung bình 31,94 giây/epoch, peak allocated 498,97 MiB; CNN 22,36 giây/epoch, 320,47 MiB. Thời gian gồm train/validation, chưa gồm ghi checkpoint/vẽ hình; bộ nhớ tensor tính bytes/1024², không phải toàn bộ VRAM driver.
- **Bằng chứng kiểm tra:** `outputs/results/task011_training_checks.json` sinh từ CSV/checkpoint và JSON cuối của hai lệnh CLI; đủ 100 dòng epoch không trùng, loss/model hữu hạn, best khớp max val Top-1 và snapshot trong last, config data/train/seed bằng nhau, đúng 450 train / 50 val mỗi lớp. Model best tải lại trên CPU qua build_model với weights_only, logits `(2,200)` hữu hạn. JSON có SHA-256 của bốn checkpoint. 72 test pass đã ghi ở TASK-006; không đổi logic train sau lần kiểm thử cuối.
- **Sản phẩm:** Checkpoint best/last cho hai model tại outputs/checkpoints (gitignore); hai CSV 50 epoch, hai PNG đường cong, JSON kiểm chứng; báo cáo mục 3.3/4.2, docs/06_training, README, phân công/tiến độ và AI_Usage đã cập nhật. Giữ nguyên mọi ghi chú chưa commit có sẵn trước buổi làm.
- **Phiên bị ngắt:** CNN vẫn chạy nền; kiểm tra PID, session và CSV rồi tiếp tục theo dõi, không khởi động trùng. Không mất epoch hoặc cần resume ở lần train thật; chức năng resume đã kiểm thử sau warmup trên cache giả trong TASK-006.
- **Giới hạn / bàn giao:** Một seed, ngân sách 50 epoch; chưa làm ablation, benchmark inference, đánh giá test, attention hoặc demo của thành viên khác. Chưa chia sẻ checkpoint ra ngoài hoặc có offsite backup. Chưa commit/push/Issue/PR/Projects do chưa được yêu cầu/quyền GitHub; mô tả local theo lựa chọn người dùng. Chờ TV1 review, không tự đánh dấu Hoàn thành.
- **Bước tiếp theo:** TV1 xem source và bằng chứng; bàn giao hai file best cho TV2/TV5, đánh giá test sau khi nhóm chốt cấu hình; tạo Issue/PR khi có quyền và commit/push khi người dùng yêu cầu.

## 2026-11-20 (TASK-008, TV2)

- **Đầu việc / Describe:** Phần còn lại của TV2: CLS attention, rollout và báo cáo. Tạo [Issue #4](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/issues/4) trước code; thông báo API mới cho demo và ngoại lệ đọc test chỉ để vẽ checkpoint đã chốt trong `docs/07_evaluation.md`, `docs/04_data.md`. Không làm TASK-007/010 hoặc merge nhánh TV4.
- **Đồng bộ:** trên `thanhbinh`, `git pull --ff-only origin main` → `59f57c8`, đã có TASK-004/005 được TV1 duyệt. Không di chuyển local `main` và không push main; nguồn train/bàn giao TV4 được đọc tại `origin/hoangdang` (`80ff9c1`) để xác minh checkpoint, không nhập code ngoài phạm vi.
- **Checkpoint / dữ liệu:** Người dùng chép checkpoint vào `outputs/checkpoints/`. ViT best nạp `weights_only=True`, strict state dict khớp factory; epoch 50, SHA-256 `97fbd0daa0e088b4b7d8a9c9adca4f61ba858986f00daa9669c83196a5a7b66b` khớp bàn giao TV4. Tải Tiny ImageNet theo script sẵn có; dừng bước dựng cache train không cần cho TASK-008, dùng lại hàm đọc nhãn/ảnh/ghi nguyên tử của `prepare_data.py` để tạo riêng 10.000 ảnh test (val gốc, 200 lớp × 50 ảnh). Tên lớp khớp repo và checkpoint. Không commit dữ liệu hoặc checkpoint.
- **Generate / Review:** `src/attention.py` có CLS layer cuối, rollout theo thứ tự thấp → cao với residual/row-normalization, resize theo config, min-max an toàn cho map hằng, overlay RGB alpha 0,5, nạp checkpoint và API `explain_image` để demo dùng lại. CLI mặc định val, test chỉ định tường minh; chọn đúng/sai cân bằng và ưu tiên lớp mới, có seed và manifest nguồn. `src/data.py` chỉ chỉnh docstring cho khớp hợp đồng, không đổi loader.
- **Run / Test / Debug:**
  - Test viết trước lỗi collection do chưa có `src.attention`; sau triển khai 20 test attention pass. Chạy `--help` phát hiện UnicodeEncodeError trên stdout cp1258, ghi [Issue #5](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/issues/5), sửa UTF-8 chỉ ở entry point CLI và thêm regression subprocess.
  - `python -m pytest -q -W error` → **73 passed in 32.69s**, gồm 21 ca attention. Ma trận tính tay kiểm thứ tự rollout và trung bình head; test map hằng/lưới khác, overlay xám/alpha, checkpoint/hash/class_names, chọn mẫu và pipeline gallery; CLI --help chạy được.
  - Chạy thật `python -m src.attention --checkpoint outputs/checkpoints/vit_small_seed42_best.pt --split test --num-images 12 --scan-limit 512 --seed 42 --device cpu --expected-sha256 97fbd0daa0e088b4b7d8a9c9adca4f61ba858986f00daa9669c83196a5a7b66b` (CPU, OMP/MKL 4 luồng) → 12 ảnh, 12 lớp, 6 đúng/6 sai. Gallery và từng ảnh đã xem trực tiếp; map float32 `(12,64,64)`, hữu hạn trong `[0,1]`, nhãn/dự đoán khớp manifest.
  - Bằng chứng: [task008_attention_checks.json](../outputs/results/task008_attention_checks.json), [manifest](../outputs/figures/attention/vit_small_seed42_test/manifest.json), [gallery](../outputs/figures/attention/vit_small_seed42_test/gallery.png). Môi trường Python 3.12.10, torch 2.15.0+cpu. Không tính Top-1/Top-5 từ tập mẫu đã chọn; file kết quả để null.
- **Explain / Documentation:** Hợp đồng và lệnh chạy ở `docs/07_evaluation.md`, README; mục 6 báo cáo có công thức, gallery, nguồn checkpoint và nhận xét định tính của ảnh đúng/sai. Sửa giới hạn phần TV2 và dòng mã nguồn attention, giữ phần TV1/TV3/TV4/TV5. Ghi nhận công cụ trong AI_Usage.
- **Giới hạn / bước tiếp theo:** Chưa kiểm tra attention CUDA/AMP, chưa làm can thiệp/định vị hoặc accuracy toàn test. Hình chọn cân bằng không đại diện accuracy. Đã commit code/hình/báo cáo `8db4115`, push riêng `fork/thanhbinh` và mở [PR #6](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/6) để TV1 review; PR đang mở, chưa merge, chưa tự đánh dấu TASK-008 hoặc bug Hoàn thành. Local `main` vẫn ở `b29de54`, main repo nhóm ở `59f57c8` do TV1 cập nhật trước buổi này. Đã thử đọc GitHub Projects nhưng API trả `INSUFFICIENT_SCOPES`, chưa cập nhật được bảng; trạng thái/bằng chứng ghi trong Issue và PR.

## 2026-11-20 (review và gộp PR #6)

- **Đầu việc:** TV1 review TASK-008 (TV2), gộp PR #6 vào `main`.
- **Kết quả / thay đổi chính:** gộp bằng merge commit để giữ commit của TV2. Dùng test để vẽ attention là đúng spec mục 229 (12 ảnh test, có đúng và sai), TV2 đã báo đổi hợp đồng ở Issue #4; code không tính accuracy test hay chọn checkpoint.
- **Bằng chứng kiểm tra:** máy TV1 (CPU): `python -m pytest -q -W error` → 73 passed; SHA-256 checkpoint `vit_small_seed42_best.pt` khớp `97fbd0da…` (epoch 50); chạy lại `python -m src.attention` cùng tham số → cùng 12 ảnh, map CLS/rollout lệch tối đa 1,3e-6 so với `maps.npz`.
- **Điều chưa xác minh:** code train của TV4 (nhánh `hoangdang`) chưa review, nên checkpoint dùng vẽ hình chưa được xác nhận quy trình; thứ tự ô hình (gốc, CLS, rollout) khác spec (gốc, rollout, CLS); chưa chạy CUDA.
- **Bước tiếp theo:** TV4 mở PR cho TASK-006/011; nếu phải train lại thì TV2 chạy lại `src.attention`.

## 2026-11-20 (review và gộp TASK-006, TASK-011)

- **Đầu việc:** TV1 review nhánh `hoangdang` của TV4 (vòng lặp train, train thật 50 epoch), gộp thẳng vào `main` không qua PR theo quyết định TV1.
- **Kết quả / thay đổi chính:** gộp bằng merge commit để giữ commit của TV4; giải xung đột ở 5 file tài liệu, giữ nội dung của cả TASK-008 (TV2) lẫn TASK-006/011 (TV4). Đọc `src/train.py`: chỉ gọi `build_loader` cho train/val, chọn best theo val Top-1, ghi file qua file tạm.
- **Bằng chứng kiểm tra:** máy TV1 (CPU): trên nhánh TV4 `python -m pytest -q -W error` → 72 passed; SHA-256 bốn checkpoint best/last khớp `task011_training_checks.json`; nạp best với `weights_only=True` và chạy lại val fp32: ViT 47,61% (log 47,63), CNN 58,74% (log 58,73); chênh do AMP trên GPU.
- **Điều chưa xác minh:** chưa chạy lại resume trên dữ liệu thật hay GPU; một số bằng chứng của TV4 trỏ vào `.git/codex/` chỉ có trên máy TV4; checkpoint chưa sao lưu ra ngoài.
- **Bước tiếp theo:** TV5 làm TASK-007 (đánh giá test) bằng hai checkpoint best; chia sẻ checkpoint cho TV5 kèm SHA-256.

## 2026-11-21 (TV5, sửa theo review TASK-007, TASK-009, TASK-010)

- **Describe:** Đọc review của TV1; kiểm tra lần lượt đánh giá/phân tích lỗi, so sánh, demo trên nhánh `vananh`. Tiếp tục các sửa đổi chưa commit có sẵn; giữ nguyên thay đổi ngoài phạm vi ở `outputs/figures/samples.png`.
- **Kết quả:** Xác minh các bản sửa đã có: khai báo Gradio 6.32.0, kiểm tra checkpoint và thông báo dễ hiểu, resize từ config, tên lớp lấy từ checkpoint, bỏ gọi phân tích lỗi/import/dòng TASK-009 trùng, đổi `test.jpg` thành `goldfish.jpg`. Bổ sung sửa nhãn lưới ảnh sai bị ẩn, biểu đồ Top-1 thiếu số liệu, backend Agg không cần Tk. Thu nhỏ ảnh khải hoàn môn từ 9.081.088 byte xuống 56.302 byte (500×331); ghi sáu URL nguồn do người dùng cung cấp vào `app/examples/README.md`.
- **Run / Test:** Python 3.13, torch 2.15.0+cpu, Gradio 6.32.0. Toàn bộ suite: **109 passed in 29.02s**, coi warning là lỗi. Lệnh thực tế: `python -X utf8 -c "import sys; sys.path.insert(0,'.test-deps'); import torch,pytest; torch.set_num_threads(2); raise SystemExit(pytest.main(['-q','-W','error','-p','no:cacheprovider','--basetemp','.pytest-tmp-review-verified']))"`. `.test-deps` chứa Pygments 2.21.0 tải tạm vì Python trên máy thiếu dependency này; tắt cacheprovider vì cache cũ bị từ chối quyền ghi. Các thư mục tạm được dọn sau kiểm tra. Khi môi trường đầy đủ, chạy `python -m pytest -q -W error -p no:cacheprovider`.
- **Kiểm tra demo thực tế:** Tạo Gradio Interface và gọi callback với hai checkpoint thật, ảnh cá vàng chuyển RGB/L/RGBA: đều trả hai bảng 5 nhãn và rollout RGB 64×64; `None` báo lỗi ảnh không hợp lệ. Không train lại hoặc dùng test chọn checkpoint. `git diff --check` đạt.
- **Debug:** Lần đầu không khởi động được pytest do thiếu Pygments; sau bổ sung dependency, gặp cache bị khóa và Tk thiếu `ttk.tcl`. Khắc phục bằng cacheprovider tắt trong lệnh kiểm tra và backend Agg cho hai script chỉ xuất PNG; lần chạy cuối exit 0.
- **Documentation / giới hạn:** Cập nhật README, tài liệu demo/đánh giá và AI_Usage; kế hoạch giữ trạng thái đã triển khai, chờ TV1 xác minh. Chưa kiểm tra lại bằng trình duyệt hoặc cài trên máy sạch; tác giả/giấy phép ảnh chưa xác nhận. Chưa cập nhật GitHub Projects; không commit, push hoặc đánh dấu Hoàn thành.
- **Bước tiếp theo:** TV1 xem diff, bằng chứng và kiểm tra demo trên máy sạch trước khi duyệt/gộp.

## 2026-11-21 (TV5, cập nhật báo cáo)

- **Bổ sung báo cáo ngày 2026-11-21 (TV5):** Cập nhật `report/report.md` phần đánh giá, so sánh, demo và kiểm thử; sửa trạng thái cũ còn ghi chưa có kết quả test, thêm MACs “chưa có”. Đối chiếu JSON kết quả ViT/CNN và comparison.csv, giữ nguyên số đo. Chạy bốn file test: **16 passed in 13.87s**.<br>
Copy project sang thư mục mới, bỏ `.git`, `.venv`, `data/` và `checkpoint`; tạo `.venv` mới, cài `requirements.txt` và chạy pytest: 109 passed.


## 2026-11-21 (TV1, review và gộp TASK-007, TASK-009, TASK-010)

- **Kết quả:** Gộp [PR #11](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/11) (nhánh `vananh`, TV5) vào `main` bằng `--no-ff`. Vòng 1 yêu cầu sửa: thiếu `gradio` trong requirements, demo in traceback khi thiếu checkpoint, ảnh mẫu 9 MB, code lặp trong `error_analysis.py`; TV5 sửa đủ và thêm 16 test. Sau gộp TV1 trả `outputs/figures/samples.png` về bản TASK-002 (TV5 vô tình đổi) và tạo `app/examples/README.md`; TV1 chấp nhận ảnh mẫu không có URL nguồn.
- **Bằng chứng:** chạy lại test trên CPU khớp 10.000/10.000 dự đoán mỗi mô hình (ViT 48,46 / 72,76, CNN 59,03 / 81,74); `scripts.error_analysis` và `src.compare` ra CSV/JSON giống hệt; callback demo với hai checkpoint thật; `python -m pytest -q -W error` trên `main` sau gộp → 109 passed.
- **Chưa xác minh:** chưa mở demo trong trình duyệt trên máy TV1; kiểm tra máy sạch của TV5 là bản copy trên cùng máy, chưa phải clone trên máy khác; giấy phép ảnh mẫu chưa xác nhận.
- **Bước tiếp theo:** TASK-012 hoàn thiện báo cáo; TV1 viết mục 1, 8, 9, tải checkpoint lấy link công khai, đi checklist "Nộp bài".

## 2026-11-22 (TV1, TASK-012 và bản nộp)

- **Kết quả:** Viết báo cáo mục 1 (vấn đề, phạm vi, chỉ số thành công) và mục 9 (trả lời hai câu hỏi, hướng phát triển); viết lại hướng dẫn cài đặt mục 8; bỏ ghi chú bản nháp, thẻ `<br>`, dòng bị ngắt và mục 6.4 Grad-CAM chưa làm. Ghi link checkpoint Google Drive và SHA-256 vào README; điền nguồn ảnh mẫu vào `app/examples/README.md` từ mục 11 báo cáo. Đi hết checklist "Nộp bài" và gắn tag bản nộp.
- **Bằng chứng:** `python -m pytest -q -W error` → 109 passed khi tạm ẩn `data/cache` và `outputs/checkpoints`; số trong báo cáo mục 2–4 đối chiếu với `dataset_stats.json`, `task004/005/011` JSON, khớp.
- **Chưa xác minh:** TV1 xác nhận link Drive đã công khai, kiểm tra máy sạch và nơi nộp; truy cập ẩn danh từ máy TV1 lúc ghi vẫn chuyển sang trang đăng nhập Google. Giấy phép ảnh mẫu chưa xác nhận.

## Mẫu buổi làm

- Ngày: [YYYY-MM-DD]
- Đầu việc: [TASK-xxx — tên]
- Kết quả / thay đổi chính: [cần điền]
- Bằng chứng kiểm tra: [lệnh → kết quả thật]
- Điều tôi giải thích được về code: [cần điền]
- Điều chưa hiểu / chưa xác minh: [cần điền]
- Bước tiếp theo: [cần điền]

## Câu hỏi cuối đầu việc
Tôi dựa vào bằng chứng nào để biết phần này đúng?

## Khi tiếp tục với AI
Đọc `AGENTS.md`, đầu việc đang làm và bản ghi mới nhất.
Xác minh trạng thái code hiện tại trước khi tiếp tục.
Không thực hiện lại việc đã hoàn thành chỉ vì phiên trò chuyện mới.
