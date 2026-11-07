# 14 — Definition of Done: kiểm tra hoàn thành và bàn giao

## Mục tiêu và đầu vào
Quyết định phần việc đã hoàn thành bằng bằng chứng: **đúng yêu cầu + code chạy + test pass**. Dùng tiêu chí đã giao, diff cuối, kết quả Run/Test, tài liệu và trạng thái Git.

## Các bước thực hiện
1. Đối chiếu từng yêu cầu trong phạm vi với hành vi đã triển khai. Không cộng tính năng ngoài phạm vi để thay thế phần còn thiếu.
2. Kiểm tra bằng chứng code chạy trong môi trường mục tiêu đã nêu; phân biệt chạy thực tế với chỉ build hoặc đọc code.
3. Kiểm tra kết quả tests/checks phù hợp; chỉ ghi pass cho lệnh/thao tác đã thực hiện.
4. Nếu có thay đổi sau lần kiểm tra cuối, xác định và chạy lại kiểm tra chịu ảnh hưởng.
5. Xác nhận không còn lỗi đã biết ngăn đáp ứng yêu cầu. Ghi rõ rủi ro/điều kiện chưa xác minh nếu còn.
6. Kiểm tra tài liệu và giải thích khớp implementation. Với phần việc có commit được giao, kiểm tra commit chứa đúng thay đổi.
7. Chọn trạng thái đúng: hoàn thành; đã triển khai nhưng chưa xác minh đủ; hoặc còn công việc cụ thể chưa xong.
8. Bàn giao ngắn, dẫn chứng đủ để người dùng đánh giá kết quả. Không chạy lại mọi check chỉ để làm dài báo cáo nếu không có lý do mới.

## Checklist kết thúc
- [ ] Yêu cầu trong phạm vi được đáp ứng.
- [ ] Code chạy được trong môi trường mục tiêu đã kiểm tra.
- [ ] Tests/checks phù hợp đã pass.
- [ ] Đã review thay đổi cuối và giữ thay đổi không liên quan của người dùng.
- [ ] Code quan trọng được giải thích.
- [ ] Tài liệu chịu ảnh hưởng đã cập nhật.
- [ ] Commit đúng phạm vi nếu được giao.
- [ ] Giới hạn còn lại được báo trung thực.

Checklist áp dụng theo phạm vi. Với nhiệm vụ chỉ PLAN hoặc tài liệu, đánh giá đầu ra đó; không yêu cầu chạy code không hề thay đổi. Điều kiện “code chạy + test pass” dành cho phần việc triển khai code.

## Đầu ra cần có
```text
Kết quả: [trạng thái có bằng chứng]
Thay đổi: [hành vi/file chính và lý do]
Kiểm chứng: [lệnh/thao tác thực tế và kết quả]
Tài liệu/commit: [nếu liên quan]
Giới hạn hoặc phần còn thiếu: [nếu có]
```

Nếu thiếu dịch vụ hoặc cấu hình để test, báo “đã triển khai, chưa xác minh ...”; không báo hoàn thành đầy đủ. Tiếp tục công việc có thể làm độc lập, yêu cầu đúng điều kiện còn thiếu khi cần.

## Prompt mẫu
```text
Dùng $vibe-coding để kiểm tra Definition of Done cho phần việc ...
Đối chiếu yêu cầu, code chạy, tests/checks và tài liệu.
Hoàn thiện phần còn thiếu trong phạm vi có thể làm,
rồi bàn giao kết quả có bằng chứng cùng giới hạn nếu còn.
```
