# 11 — Commit: chốt phần việc đã xác minh

## Mục tiêu và đầu vào
Lưu một phần việc rõ nghĩa bằng Git sau khi đã kiểm chứng. Dùng diff cuối, kết quả checks và phạm vi commit được giao.

## Các bước thực hiện
1. Kiểm tra việc commit có nằm trong yêu cầu/quyền đã có của nhiệm vụ hay không. Skill này không tự cấp quyền commit mọi project tương lai.
2. Xem `git status` và diff; phân biệt thay đổi của nhiệm vụ với thay đổi có sẵn của người dùng.
3. Kiểm tra code, tests và tài liệu cần cho phần việc này đã nhất quán. Nếu refactor hoặc sửa lỗi sau lần test trước, chạy lại checks chịu ảnh hưởng.
4. Chọn file/hunk của nhiệm vụ để stage. Không stage toàn bộ repo một cách máy móc khi có thay đổi không liên quan.
5. Xem staged diff; bảo đảm nội dung staged chính là phần đã review và kiểm tra, không kèm file tạm hay dữ liệu riêng tư.
6. Viết commit message mô tả kết quả cụ thể, ví dụ `fix: reject empty item names`; theo convention của repo nếu có.
7. Khi đã được giao commit, tạo commit và kiểm tra kết quả, hash và trạng thái repo sau đó.
8. Không tự push, merge, deploy hay sửa lịch sử để làm đẹp kết quả. Nếu hook thất bại, xử lý theo bằng chứng, không bỏ qua checks chỉ để commit thành công.

## Đầu ra cần có
- Nếu đã commit: hash, message và phạm vi thay đổi.
- Checks đã thực hiện cho phần việc.
- Thay đổi còn lại ngoài commit nếu có, không tự nhận repo sạch.
- Nếu nhiệm vụ chưa bao gồm commit: diff đã kiểm chứng, sẵn sàng để người dùng review; không báo đã tạo commit.

## Điều kiện chuyển bước
- Phần việc được chốt đúng phạm vi và có bằng chứng kiểm chứng.
- Không đưa thay đổi không liên quan của người dùng vào commit.
- Giải thích và tài liệu chịu ảnh hưởng đã cập nhật hoặc tiếp tục hoàn thiện trước bàn giao.

## Prompt mẫu
```text
Dùng $vibe-coding để review và commit phần việc ... đã kiểm chứng.
Chỉ stage file/hunk thuộc nhiệm vụ, giữ thay đổi khác của tôi.
Theo convention của repo, báo commit hash và kết quả kiểm tra.
```
