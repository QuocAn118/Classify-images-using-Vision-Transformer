# Kế hoạch và phân công

File này giữ phân công, danh sách đầu việc, mốc và quy tắc cắt việc; ít khi thay đổi. **Trạng thái từng đầu việc theo dõi trên GitHub**, không ghi ở đây.

## Phân công

| Thành viên | Vai trò | Tài liệu giữ | Phần báo cáo (mục 15 spec) |
|---|---|---|---|
| TV1 | Trưởng nhóm, dữ liệu, tài liệu | [04_data.md](04_data.md), [01_define.md](01_define.md), [02_architecture.md](02_architecture.md), file này | 1, 2, 8, 9 |
| TV2 | ViT và attention | [05_model.md](05_model.md) phần ViT, phần attention trong [07_evaluation.md](07_evaluation.md) | 3 (ViT), 6 |
| TV3 | CNN, đo FLOPs/MACs | [05_model.md](05_model.md) phần CNN | 3 (CNN), 6 (Grad-CAM nếu có) |
| TV4 (Hđang) | Huấn luyện | [06_training.md](06_training.md) | 4 |
| TV5 | Đánh giá, demo, ghép báo cáo | [07_evaluation.md](07_evaluation.md), [08_demo.md](08_demo.md) | 5, 7, 10 |

TV1 là trưởng nhóm/chủ repo; TV4 là Hđang theo phân công nhóm người dùng cung cấp ngày 2026-11-19. Máy TV4 hiện kiểm tra được RTX 5060 Laptop 8GB; giả định GPU 6GB trong kế hoạch cần phân biệt với phép đo máy này.

## Theo dõi trạng thái trên GitHub
- Mỗi đầu việc là một **Issue**, tạo từ mẫu `.github/ISSUE_TEMPLATE/task.md`. Phần mô tả đầu việc (bước Describe) viết trong Issue.
- Trạng thái theo dõi trên bảng **GitHub Projects** với các cột: Chưa bắt đầu → Đang làm → Đã triển khai, chưa xác minh → Hoàn thành. Dùng nhãn `bi-chan` kèm comment nêu nguyên nhân nếu thiếu điều kiện.
- Mỗi PR ghi `Closes #<số issue>`. PR theo mẫu `.github/pull_request_template.md`, có phần Review, Test và bằng chứng.
- Chỉ chuyển sang Hoàn thành khi PR đã có bằng chứng kiểm tra và người duyệt đã xem. AI báo xong chưa đủ.
- Lỗi phát sinh tạo Issue từ mẫu `.github/ISSUE_TEMPLATE/bug.md`.

**Hiện trạng:** Issue và bảng Projects chưa tạo. Cho đến khi tạo: TASK-000 hoàn thành (nhóm duyệt `docs/` ngày 2026-11-15); TASK-014 hoàn thành (đã nộp mẫu đăng ký, TV1 báo ngày 2026-11-15); TASK-001 hoàn thành (12 test pass, TV1 đọc code ngày 2026-11-16); TASK-002 hoàn thành (18 test pass, chạy trên dữ liệu thật, TV1 đọc code ngày 2026-11-17); TASK-003 hoàn thành (25 test pass, TV1 đọc code ngày 2026-11-17); TASK-004 hoàn thành (TV2, PR #2 gộp ngày 2026-11-17, 48 test pass); TASK-005 hoàn thành (TV3, PR #3 gộp ngày 2026-11-19, 52 test pass); TASK-008 hoàn thành (TV2, PR #6 gộp ngày 2026-11-20, 73 test pass, hình từ checkpoint TV4 bàn giao; nếu train lại thì chạy lại `src.attention`); TASK-006 và TASK-011 hoàn thành (TV4, nhánh `hoangdang` gộp ngày 2026-11-20 không qua PR theo yêu cầu TV1; TV1 chạy lại val từ checkpoint khớp log); TASK-007, TASK-009 và TASK-010 hoàn thành (TV5, [PR #11](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/11) gộp ngày 2026-11-21, 109 test pass; TV1 chạy lại đánh giá test khớp 10.000/10.000 dự đoán mỗi mô hình, chạy lại `scripts.error_analysis` và `src.compare` ra CSV/JSON giống hệt, gọi callback demo với hai checkpoint thật); các đầu việc còn lại chưa xác nhận hoàn thành.

## Danh sách đầu việc

| Mã | Đầu việc | Phụ trách | Yêu cầu | Phụ thuộc |
|---|---|---|---|---|
| TASK-000 | Hoàn thiện `docs/` | TV1 | Quy trình `workflow/` | Không |
| TASK-014 | Nộp mẫu đăng ký (mục 21 spec) | TV1 | Đề | Nhóm chốt TV |
| TASK-001 | Khung repo và tiện ích dùng chung | TV1 | AC-013, một phần AC-008 | TASK-000 |
| TASK-002 | Chuẩn bị dữ liệu, chia tập, xuất mảng cache | TV1 | FR-001 | TASK-001, có file dữ liệu |
| TASK-003 | DataLoader đọc mảng cache, augmentation | TV1 | FR-001 | TASK-002 |
| TASK-004 | ViT và test | TV2 | FR-002 | TASK-001 |
| TASK-005 | CNN và `match_param_count` | TV3 | FR-003 | TASK-004 |
| TASK-006 | Vòng lặp train, `--quick`, `--resume` | TV4 | FR-004 | TASK-001, 003, 004, 005 |
| TASK-007 | Đánh giá và phân tích lỗi | TV5 | FR-005 | TASK-006 |
| TASK-008 | Trực quan hóa attention | TV2 | FR-006 | Code và test: TASK-004 (làm được ngay, dùng mô hình trọng số ngẫu nhiên); hình thật: checkpoint từ TASK-011 |
| TASK-009 | Bảng so sánh | TV5 | FR-007 | TASK-007 |
| TASK-010 | Demo | TV5 | FR-008 | TASK-006 |
| TASK-011 | Train thật ViT và CNN | TV4 | FR-004 | TASK-006, máy GPU của thành viên sẵn sàng |
| TASK-012 | Đánh giá test cuối và báo cáo | TV5, cả nhóm | FR-005, 007, 009 | TASK-011 |
| TASK-013 | Phần làm thêm theo thứ tự cắt việc dưới đây | Theo phần | Không bắt buộc | TASK-011 |

**Điều kiện bắt đầu code:** Chỉ bắt đầu TASK-001 và các đầu việc code khác sau khi nhóm duyệt `docs/`. Bản thử đầu của TASK-001 viết sai thứ tự nên đã bị xóa.

**Đầu việc tiếp theo:** TASK-001 đến 011 xong. TASK-012 (TV5, cả nhóm): hoàn thiện báo cáo từ số test đã có, không chạy lại test để chọn gì. TV1 viết mục 1, 8, 9, tải checkpoint lấy link công khai và đi checklist "Nộp bài". TASK-013 chỉ làm nếu còn thời gian. TV1 làm thẳng trên `main` (DEC-014). Không dùng test để chọn checkpoint hoặc siêu tham số.

## Mốc và lịch

| Mốc | Kết quả trình diễn được | Đầu việc | Hạn |
|---|---|---|---|
| M0 | `docs/` được nhóm duyệt, đã nộp mẫu đăng ký (xong 15/11) | 000, 014 | 15/11 |
| M1 | Khung repo và hợp đồng sẵn sàng | 001 | 16/11 |
| M2 | `--quick` chạy thông từ dữ liệu đến checkpoint | 002-006 | 17/11 |
| M3 | Có checkpoint thật, đủ công cụ đánh giá và demo | 007-011 | 20/11 |
| M4 | Có số cuối trên test, dừng mọi thí nghiệm | 012, 013 | 21/11 |
| M5 | Báo cáo khớp số liệu, nộp bài | 012 | 24/11 |

Hạn nộp 25/11 (giảng viên gia hạn từ 20/11); 25/11 để dự phòng. Lịch cũ nhắm 19/11 đã trễ từ M0. Quy tắc cắt việc khi trễ ở mục 20 của spec.

## Thứ tự cắt việc khi trễ
CNN thứ hai có FLOPs xấp xỉ ViT, rồi ablation, rồi 3 seed, rồi Grad-CAM, cuối cùng mới đến đo FLOPs/MACs (TV3 phụ trách). Thí nghiệm SGD được cắt cùng lúc với CNN thứ hai; attention theo head và layer được cắt cùng lúc với Grad-CAM. Giữ nguyên bộ lõi: ViT, CNN, attention, demo, báo cáo. Không giảm dưới 50 epoch (DEC-008).

## Nộp bài (Definition of Done)

Với đồ án này, "phát hành" là bản nộp cho giảng viên. Chưa có bản nộp.

**Trước khi nộp:**
- [ ] Tiêu chí trong phạm vi đã có bằng chứng kiểm tra.
- [ ] Hạn chế và phần chưa xác minh được nêu rõ.
- [ ] README khớp cách chạy thật.
- [ ] Môi trường và dữ liệu cần thiết đã được kiểm tra trên máy sạch.
- [ ] Mọi số trong báo cáo khớp với file kết quả.
- [x] Link checkpoint mở được khi không đăng nhập tài khoản của nhóm. TV1 xác nhận đã mở quyền chia sẻ thư mục [Google Drive](https://drive.google.com/drive/folders/1tt17rM1VGNZwshr4-DTt4OMNHc0IA6BE?usp=drive_link) ngày 2026-11-22; link và SHA-256 ghi trong README.
- [x] Repo không chứa `kaggle.json`, dữ liệu hoặc checkpoint. TV1 kiểm `git ls-files` ngày 2026-11-22: không có `.pt`, `.npy`, `data/`, `kaggle.json`; chỉ có `maps.npz` là map attention dẫn xuất của TASK-008.
- [ ] Có commit hoặc tag đánh dấu bản nộp để quay lại khi cần.
- [ ] Đã xác nhận nơi và hình thức nộp bài.

**Bản nộp:**
- **Phiên bản / commit:** Chưa có
- **Nơi truy cập:** GitHub `QuocAn118/Classify-images-using-Vision-Transformer`; nơi nộp chính thức chưa xác nhận
- **Sản phẩm bàn giao:** Mã nguồn, checkpoint, bảng so sánh, hình attention, phân tích lỗi, demo, báo cáo
- **Cách quay lại bản trước:** Checkout commit hoặc tag đã đánh dấu

**Sau khi nộp, thử lại:**

| Luồng cần thử | Kết quả thực tế | Bằng chứng |
|---|---|---|
| Copy mới, cài đặt, chạy `pytest` | Đã chạy trên môi trường Python mới cùng máy | 109 passed tại `D:\Classify-images-clean-check`; chi tiết tại `docs/10_work_log.md` |
| Tải checkpoint, chạy `app/demo.py`, thử một ảnh | Đã thử cùng môi trường mới; không copy `data/` | Hướng dẫn và giới hạn ghi tại `docs/10_work_log.md` |
| Chạy `src.compare`, đối chiếu với báo cáo | TV1 chạy lại 2026-11-21, CSV/MD giống hệt bản commit; số mục 5, 7 báo cáo khớp file | [PR #11](https://github.com/QuocAn118/Classify-images-using-Vision-Transformer/pull/11), `docs/10_work_log.md` |

Phản hồi của giảng viên ghi vào [10_work_log.md](10_work_log.md); đầu việc phát sinh tạo Issue mới.
