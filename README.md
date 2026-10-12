# Tổng hợp Bài tập Thực hành Python

Thư mục này bao gồm toàn bộ bài tập thực hành theo yêu cầu:

---

### 1. [lab4/](file:///Users/duongnad/Documents/Aptech/Python/lab4/) (Bài tập Lab 4 - File I/O, Threading, JSON & Pickle)
Bao gồm đầy đủ 10 bài tập độc lập và script chạy tổng hợp:
- [`bai1.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai1.py): Ghi và đọc file văn bản (`sentences.txt`), đếm số dòng, in câu dài nhất.
- [`bai2.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai2.py): Đếm từ trong file `story.txt`, chuẩn hoá chữ thường & dấu câu, xuất top 5 từ ra `summary.txt`.
- [`bai3.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai3.py): Copy file lớn (`source.txt` $\rightarrow$ `target.txt`) bằng Thread, hiển thị tiến độ byte, so sánh thời gian, kiểm tra MD5.
- [`bai4.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai4.py): 3 thread cùng ghi 30 dòng vào `logs.txt` với `threading.Lock` an toàn.
- [`bai5.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai5.py): Luồng theo dõi thay đổi file `watched.txt` mỗi 3s, luồng giả lập user ghi thêm, tự dừng sau 30s.
- [`bai6.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai6.py): Quản lý danh sách sinh viên qua `students.json` (Serialize / Deserialize).
- [`bai7.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai7.py): Quản lý công việc ToDo bằng JSON (`todo.json`), bắt lỗi FileNotFoundError & JSONDecodeError.
- [`bai8.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai8.py): Lưu trạng thái đối tượng `GameState` vào `state.dat` bằng `pickle`, xác minh tính toàn vẹn.
- [`bai9.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai9.py): Giao tiếp giữa Hàm A (tạo JSON) và Hàm B (đọc JSON, ép kiểu float giá tiền, tính tiền 3 sản phẩm).
- [`bai10.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai10.py): Chuyển đổi dữ liệu `products.csv` thành `products.json` với trường Price là số float.
- [`run_all.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/run_all.py): Script kiểm thử tự động toàn bộ 10 bài.

---

### 2. [lab5_yolo_detection/](file:///Users/duongnad/Documents/Aptech/Python/lab5_yolo_detection/) (Bài tập Lab 5 - YOLO Object Detection)
- **Chủ đề:** FastAPI + YOLOv8 + Upload/Detect.
- Tuyến `POST /upload` nhận ảnh (`form-data`), lưu vào `uploads/`, chạy YOLOv8, vẽ bounding box, phản hồi `image/jpeg`.
- Tuyến `GET /classes` trả về 80 nhãn đối tượng.
- Giới hạn file $\le$ 5MB, hỗ trợ `.jpg`, `.jpeg`, `.png`.
- Ghi log thành công vào `detection.log`.
- Giao diện Web kiểm thử kéo thả ảnh tại `http://localhost:8001/`.

---

### 3. [lab6_user_system/](file:///Users/duongnad/Documents/Aptech/Python/lab6_user_system/) (Bài tập Lab 6 - Quản lý Người dùng MySQL)
- **Chủ đề:** Python + MySQL + FastAPI + Jinja2.
- Tự động tạo CSDL `user_system` và bảng `users`.
- Cung cấp đầy đủ REST API CRUD (`/api/users`).
- Giao diện Web HTML Form với Bootstrap 5 (`/users`, `/users/add`, `/users/edit/{id}`, `/users/delete/{id}`).
- Mã hoá mật khẩu bằng **Bcrypt**, hiển thị ngày tạo theo chuẩn `DD/MM/YYYY HH:MM`.
- Ghi log vào file `app.log`.
- Nạp 5 người dùng mẫu ban đầu bằng `python3 init_db.py`.
- Khởi chạy trên cổng 8000: `http://localhost:8000/users`.
