# Sercurity requirements cho json_search()
Dựa trên phân tích Threat Model, các yêu cầu an toàn phải được hiện thực:
1. **Role-Based Access Control:** 
   Hàm `json_search` phải nhận thông tin vai trò người dùng `role`. Hệ thống chỉ trả về giá trị của trường tìm kiếm nếu `role` hiện tại nằm trong danh sách các vai trò được phép quy định tại `policy.py`.
2. **Principle of Least Privilege & Default Deny:**
   - Nếu `role=None` hoặc role không hợp lệ khi tra cứu các trường `apiKey`, `managementIpAddress`, `issueSummary`, hàm phải từ chối trả về dữ liệu (trả về danh sách rỗng `[]`).
   - Trường `apiKey` chỉ cho phép vai trò `admin` truy cập.
   - Trường `managementIpAddress` chỉ cho phép vai trò `admin` và `operator` truy cập. Vai trò `viewer` không được phép xem.
   - Trường `issueSummary` cho phép cả 3 vai trò: `admin`, `operator`, `viewer`.
3. **Automated Security Testing:**
   Mọi quy định về phân quyền ở SR-01 và SR-02 phải có unit test kiểm thử bảo mật tương ứng và phải vượt qua 100% trước khi triển khai.
