# Sercurity requirements cho json_search()
Dựa trên phân tích Threat Model, các yêu cầu an toàn phải được hiện thực:
1. **Recursive search và Role-Based Access Control:**
   Hàm `json_search` phải tìm đệ quy trong dictionary và list, trả về tất cả giá trị khớp mà không bỏ sót kết quả. Với các trường được quy định trong `policy.py`, chỉ trả về kết quả nếu `role` hiện tại nằm trong danh sách vai trò được phép.
2. **Principle of Least Privilege & Default Deny:**
   - Nếu `role=None` hoặc role không hợp lệ khi tra cứu các trường `apiKey`, `managementIpAddress`, `issueSummary`, hàm phải từ chối trả về dữ liệu (trả về danh sách rỗng `[]`).
   - Trường `apiKey` chỉ cho phép vai trò `admin` truy cập.
   - Trường `managementIpAddress` chỉ cho phép vai trò `admin` và `operator` truy cập. Vai trò `viewer` không được phép xem.
   - Trường `issueSummary` cho phép cả 3 vai trò: `admin`, `operator`, `viewer`.
   - Trường không được khai báo trong `policy.py` không thuộc phạm vi phân quyền của các quy tắc trên.
3. **Automated Security Testing:**
   Mọi quy định về phân quyền ở SR-01 và SR-02 phải có unit test kiểm thử bảo mật tương ứng và phải vượt qua 100% trước khi triển khai.
