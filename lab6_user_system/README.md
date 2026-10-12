# Bài 1 (Lab 6) - Xây dựng hệ thống quản lý người dùng kết nối MySQL, cung cấp API và Web

Dự án hoàn chỉnh theo yêu cầu đề bài: **Python + MySQL + FastAPI + Jinja2**.

---

## 📋 Yêu cầu đã hiện thực

### A. Database (MySQL)
- [x] Tạo cơ sở dữ liệu tên `user_system`.
- [x] Tạo bảng `users` gồm các cột: `id`, `name`, `email`, `password`, `created_at`.
- [x] Thiết lập kết nối tới MySQL từ Python (`mysql-connector-python`).
- [x] Tạo hàm khởi tạo DB tự động, tự tạo DB và bảng nếu chưa tồn tại (`init_db()`).

### B. API (FastAPI)
- [x] `GET /api/users`: Trả về danh sách người dùng.
- [x] `GET /api/users/{id}`: Lấy thông tin 1 người dùng.
- [x] `POST /api/users`: Tạo người dùng mới qua JSON payload.
- [x] `PUT /api/users/{id}`: Cập nhật thông tin người dùng.
- [x] `DELETE /api/users/{id}`: Xoá người dùng.
- [x] Validate email trùng lặp $\rightarrow$ Trả về mã lỗi HTTP 400.

### C. Web UI (Jinja2 + HTML Form)
- [x] Route `/users`: Hiển thị bảng danh sách người dùng trực quan, có tìm kiếm tức thời.
- [x] Route `/users/add`: Form thêm người dùng mới và xử lý POST.
- [x] Route `/users/edit/{id}`: Form chỉnh sửa người dùng và xử lý POST.
- [x] Route `/users/delete/{id}`: Trang xác nhận xoá an toàn và xử lý xoá.
- [x] Tạo template `base.html` và kế thừa template cho tất cả các trang con.

### D. Bảo mật & Tiện ích
- [x] Mã hoá mật khẩu bằng **Bcrypt**.
- [x] Định dạng thời gian tạo người dùng theo chuẩn: `DD/MM/YYYY HH:MM`.
- [x] Sử dụng **Bootstrap 5.3**, Bootstrap Icons và CSS hiện đại, responsive trên mobile/desktop.

### E. Khác
- [x] Ghi nhật ký hành động vào file `app.log` khi có thao tác thêm/sửa/xoá.
- [x] Tạo file `init_db.py` để khởi tạo 5 người dùng mẫu ban đầu (kèm mật khẩu đã băm).

---

## 🚀 Cấu trúc thư mục

```text
lab6_user_system/
├── templates/
│   ├── base.html                  # Template khung chung (Bootstrap 5, Navbar, Flash messages)
│   └── users/
│       ├── index.html             # Danh sách người dùng + tìm kiếm
│       ├── add.html               # Form thêm người dùng
│       ├── edit.html              # Form sửa người dùng
│       └── delete_confirm.html    # Trang xác nhận xoá
├── static/
├── .env                           # File biến môi trường cấu hình DB
├── .env.example                   # File mẫu biến môi trường
├── docker-compose.yml             # Khởi chạy MySQL container nhanh chóng
├── requirements.txt               # Danh sách thư viện cần thiết
├── config.py                      # Đọc biến môi trường
├── logger.py                      # Thiết lập log ra app.log và console
├── database.py                    # Kết nối MySQL & hàm init_db()
├── auth.py                        # Hàm mã hoá bcrypt và verify mật khẩu
├── schemas.py                     # Pydantic schemas cho API
├── crud.py                        # Các hàm thao tác dữ liệu với MySQL
├── init_db.py                     # Script nạp 5 người dùng mẫu
├── main.py                        # Ứng dụng chính FastAPI & Jinja2
├── app.log                        # File lưu vết hoạt động thêm/sửa/xoá
└── README.md                      # Hướng dẫn chi tiết
```

---

## 🛠 Hướng dẫn cài đặt & Khởi chạy

### 1. Cài đặt các thư viện cần thiết
```bash
pip install fastapi uvicorn jinja2 mysql-connector-python passlib[bcrypt] bcrypt python-dotenv python-multipart
```

### 2. Khởi chạy MySQL Database
Nếu bạn dùng Docker:
```bash
docker compose up -d
```
Hoặc kết nối tới MySQL có sẵn trên máy của bạn (chỉnh thông tin trong file `.env`):
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=user_system
```

### 3. Nạp dữ liệu 5 người dùng mẫu (Test Data)
Chạy lệnh:
```bash
python3 init_db.py
```

### 4. Khởi chạy Web & API Server
```bash
uvicorn main:app --reload --port 8000
```

### 5. Truy cập ứng dụng
- **Giao diện Web:** Mở trình duyệt tại [http://localhost:8000/users](http://localhost:8000/users)
- **Tài liệu API (Swagger UI):** Mở trình duyệt tại [http://localhost:8000/docs](http://localhost:8000/docs)
- **Kiểm tra file Log:** Mở xem file `app.log` khi thực hiện thêm/sửa/xoá người dùng.
