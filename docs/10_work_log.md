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
