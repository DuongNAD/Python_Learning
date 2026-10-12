# Bài 2 (Lab 5) - Xây dựng YOLO API: Nhận diện object từ ảnh người dùng upload

Dự án hoàn chỉnh theo yêu cầu đề bài: **FastAPI + YOLOv8 + Upload/Detect**.

---

## 📋 Yêu cầu đã hiện thực

- [x] Tạo route `POST /upload` nhận ảnh từ người dùng (`form-data`).
- [x] Lưu ảnh tạm vào thư mục `uploads/`.
- [x] Load mô hình YOLO (sử dụng YOLOv8 từ thư viện `ultralytics`).
- [x] Chạy nhận diện object trên ảnh vừa upload.
- [x] Vẽ bounding boxes vào ảnh đầu ra.
- [x] Trả ảnh đã nhận diện dạng `image/jpeg` trong response.
- [x] (Tùy chọn) API `GET /classes`: trả danh sách các object nhận diện được.
- [x] Hạn chế upload file dung lượng > 5MB (trả lỗi HTTP 400).
- [x] Kiểm tra định dạng file hợp lệ: `.jpg`, `.jpeg`, `.png` (trả lỗi HTTP 400).
- [x] Ghi log các lần nhận diện thành công vào file `detection.log`.
- [x] Tích hợp sẵn giao diện Web tương tác trực quan tại route `GET /` để kéo thả ảnh và xem kết quả ngay trên trình duyệt.

---

## 🚀 Cấu trúc thư mục

```text
lab5_yolo_detection/
├── templates/
│   └── index.html             # Giao diện Web kiểm thử kéo thả ảnh và xem kết quả
├── uploads/                   # Thư mục lưu ảnh upload tạm thời
├── main.py                    # Ứng dụng FastAPI xử lý upload & chạy YOLO
├── detection.log              # File lưu lịch sử các lần nhận diện thành công
├── requirements.txt           # Danh sách thư viện cần thiết
└── README.md                  # Hướng dẫn chi tiết
```

---

## 🛠 Hướng dẫn cài đặt & Khởi chạy

### 1. Cài đặt các thư viện cần thiết
```bash
pip install fastapi uvicorn python-multipart opencv-python pillow ultralytics
```

### 2. Khởi chạy Server
```bash
uvicorn main:app --reload --port 8001
```

### 3. Kiểm thử ứng dụng

#### Cách 1: Sử dụng Giao diện Web trực quan (Khuyên dùng)
- Truy cập vào: [http://localhost:8001/](http://localhost:8001/)
- Kéo thả file ảnh hoặc chọn file từ máy tính $\rightarrow$ Bấm **"Nhận diện Vật thể"**.
- Trình duyệt sẽ hiển thị ngay ảnh kết quả có bounding boxes và nút tải ảnh về máy.

#### Cách 2: Gọi API qua Swagger UI
- Truy cập vào: [http://localhost:8001/docs](http://localhost:8001/docs)
- Test endpoint `POST /upload` với file ảnh bất kỳ.
- Test endpoint `GET /classes` để xem danh sách 80 classes được hỗ trợ.

#### Cách 3: Sử dụng cURL từ Terminal
```bash
curl -X POST "http://localhost:8001/upload" \
     -H "accept: image/jpeg" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/duong/dan/anh_cua_ban.jpg" \
     --output ket_qua.jpg
```

### 4. Kiểm tra file Log
Xem các lần nhận diện thành công trong file `detection.log`:
```bash
cat detection.log
```
Mỗi dòng log ghi rõ: Thời gian, Tên file, Kích thước file, Số lượng đối tượng và Danh sách các đối tượng phát hiện được kèm tỉ lệ phần trăm chính xác (confidence).
