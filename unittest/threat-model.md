# THREAT MODEL cho hàm json_search()
Áp dụng mô hình STRIDE
## 1. Context và Scope
Hàm `json_search(key, input_object)` được sử dụng bởi dịch vụ nội bộ để trích xuất dữ liệu từ các phản hồi API giám sát hạ tầng mạng.
## 2. Các thành phần theo yêu cầu đề bài
### (a) Actors / Roles và mục đích sử dụng
- **Admin:** Toàn quyền tra cứu thông tin, cấu hình thiết bị, quản lý mã khóa API và khắc phục sự cố.
- **Operator:** Tra cứu tình trạng thiết bị, địa chỉ IP quản trị `managementIpAddress` và mã lỗi để xử lý sự vụ kỹ thuật hàng ngày.
- **Viewer:** Nhân viên giám sát cơ bản, chỉ được xem tóm tắt sự việc `issueSummary` và thống kê mức độ cảnh báo, không được can thiệp.
### (b) Sensitive Assets trong test_data.py
- **Critical Secret:** `apiKey`, `snmpCommunity`. Những chuỗi bí mật xác thực có thể bị kẻ tấn công lợi dụng để chiếm quyền điều khiển thiết bị mạng.
- **Confidential Asset:** `managementIpAddress`. Địa chỉ IP nội bộ của core switch/router, để lộ sẽ hỗ trợ kẻ tấn công lập bản đồ mạng và dò quét port.
- **Internal Asset:** `issueSummary`, `category`, `id` là các thông tin vận hành.
### (c) Trust Boundary
- **Ranh giới:** giữa người dùng gọi API (User Context) và tầng dữ mạng.
- **Lỗ hổng Trust Boundary:** Hàm `json_search()` cho phép bất kỳ caller nào truy xuất mọi trường dữ liệu mà không hề xác thực hay kiểm tra vai trò. Bất kỳ ai có quyền truy cập hàm đều đọc được tài sản tối mật.
### (d) STRIDE Mapping
- **Information Disclosure - Nguy cơ chính:**
  - *Mô tả:* Người dùng role `viewer` gọi `json_search("apiKey", data)` hoặc `json_search("managementIpAddress", data)` và nhận được khóa xác thực hoặc IP hạ tầng.
  - *Hậu quả:* Lộ secret dẫn đến nguy cơ rò rỉ toàn bộ hệ thống mạng.
- **Elevation of Privilege:**
  - *Mô tả:* Kẻ tấn công có tài khoản `viewer`, lợi dụng việc thiếu kiểm soát truy cập tại hàm để lấy được `apiKey` của `admin`, từ đó mạo danh quản trị viên thực thi lệnh trên thiết bị.
## 3. Ma trận STRIDE
| Ký hiệu | Mối đe dọa | Bối cảnh trong json_search | Mức độ |
|---|---|---|---|
| Spoofing | Giả mạo danh tính | Caller truyền role giả nếu không có auth token | Cao |
| Tampering | Sửa đổi dữ liệu | Dữ liệu trả về bị can thiệp nếu bộ nhớ chia sẻ | Thấp |
| Repudiation | Chối bỏ trách nhiệm | Không có logging ai đã trích xuất `apiKey` | Trung bình |
| Information Disclosure | Lộ lọt thông tin | Viewer xem được apiKey và IP quản lý | Rất cao |
| Denial of Service | Từ chối dịch vụ | JSON lồng nhau vô hạn gây tràn Stack | Trung bình |
| Elevation of Privilege| Leo thang đặc quyền | Dùng apiKey đánh cắp để chiếm quyền admin | Rất cao |
