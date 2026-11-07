# Sơ đồ quy trình

Sơ đồ là đường dẫn để làm việc, không phải danh sách phải điền đủ bất kể quy mô.
Lưu đồ dưới đây thể hiện vòng lặp kiểm chứng.

```mermaid
flowchart TD
    A["Define và yêu cầu"] --> B["Khảo sát và thiết kế"]
    B --> C["Breakdown và công cụ"]
    C --> D["Triển khai một đầu việc"]
    D --> E["Kiểm tra code, thiết kế và kết quả"]
    E --> F{"Đạt tiêu chí?"}
    F -->|Chưa| D
    F -->|Đạt| G{"Còn đầu việc?"}
    G -->|Có| D
    G -->|Hết| H["Phát hành và theo dõi"]
```

## Dùng file nào ở thời điểm nào?
| Thời điểm | File cần dùng |
| --- | --- |
| Bắt đầu dự án | README.md; 01_DEFINE; 02_REQUIREMENTS |
| Chọn phương án | 03_DESIGN; 05_TOOLS |
| Chuẩn bị triển khai | AGENTS.md; 04_BREAKDOWN |
| Code, debug, kiểm tra | 04_BREAKDOWN; 06_VERIFICATION |
| Kết thúc buổi | 07_WORK_LOG |
| Phát hành | 08_RELEASE |

Nếu kiểm tra cho thấy yêu cầu hoặc thiết kế sai, quay lại cập nhật phần đó; không chỉ sửa code.
