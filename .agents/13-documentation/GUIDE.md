# 13 — Documentation: tài liệu project và việc dùng AI

## Mục tiêu và đầu vào
Giữ mô tả, hướng dẫn sử dụng và ghi nhận AI khớp với project thực tế. Dùng Define/Design/Plan, code hiện tại, lệnh đã chạy và lịch sử hỗ trợ đã biết.

## Các bước thực hiện
1. Đọc tài liệu hiện có và quy ước repo; cập nhật đúng nơi, tránh tạo bản sao mâu thuẫn.
2. Ghi `Project_description.md` từ giai đoạn chuẩn bị, cập nhật khi phạm vi hoặc thiết kế thay đổi.
3. Tạo/cập nhật `README.md` khi cần giới thiệu, chạy hoặc bàn giao project.
4. Ghi `AI_Usage.md` với công cụ thực sự dùng, mục đích và đóng góp đã xác định.
5. Kiểm tra paths, tên scripts, commands và mô tả API so với code. Không đưa lệnh chưa xác nhận vào tài liệu như đã chạy thành công.
6. Nêu điều kiện môi trường, giới hạn hoặc phần chưa hoàn thành khi ảnh hưởng người dùng.
7. Review tài liệu cùng code, giữ thuật ngữ và tính năng nhất quán.

## Cấu trúc tài liệu

### Project_description.md
- **Define:** project name, problem, target users, input/output, core features, tech constraints, evaluation criteria, phạm vi và giả định.
- **Design:** system architecture, models, folder structure, data flow, interfaces/APIs, technical risks.
- **Plan:** modules, dependencies, milestones, tiêu chí kiểm chứng và trạng thái thực tế.

### README.md
- Project overview.
- Problem statement.
- Main features.
- System architecture.
- Hướng dẫn chuẩn bị/chạy và kiểm tra dựa trên repo thực tế.
- Giới hạn ảnh hưởng việc dùng project nếu có.

Bốn mục đầu lấy từ ghi chú; hướng dẫn chạy/kiểm tra là phần bổ sung để bàn giao dùng được.

### AI_Usage.md
| Tools used | Main purposes | AI hỗ trợ | Đóng góp sinh viên/người thực hiện |
| --- | --- | --- | --- |
| Tên công cụ đã dùng | Mục đích cụ thể | Phần việc đã biết | Phần đóng góp được xác nhận |

Ghi trung thực, không bịa công cụ hay đóng góp của người dùng. Nếu chưa biết phần đóng góp, ghi “chưa xác nhận” và chỉ hỏi khi thông tin đó cần cho bàn giao. Không tự nhận toàn bộ code do sinh viên viết.

## Đầu ra cần có
Tài liệu chịu ảnh hưởng được cập nhật; project mới có ba file trên ở mức phù hợp. Với repo hiện có, tôn trọng tên/vị trí tương đương thay vì bắt buộc đổi cấu trúc.

## Điều kiện chuyển bước
- Nội dung khớp code, phạm vi và kết quả kiểm chứng hiện tại.
- Người khác có thể xác định cách chạy/kiểm tra và vai trò AI từ tài liệu.
- Không chờ đến cuối project mới ghi Define/Design hoặc kế hoạch.

## Prompt mẫu
```text
Dùng $vibe-coding để cập nhật tài liệu theo project hiện tại.
Kiểm tra Project_description.md, README.md và AI_Usage.md
hoặc tài liệu tương đương của repo. Dùng lệnh đã xác nhận,
ghi trung thực công cụ AI và đóng góp, nêu phần chưa có thông tin.
```
