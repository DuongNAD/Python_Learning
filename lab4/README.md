# Bài tập Lab 4 - Python File I/O, Threading, JSON & Pickle

Tổng hợp 10 bài tập thực hành theo yêu cầu của **Bài tập lab 4**.

---

## 📋 Danh sách các bài tập

| STT | File | Nội dung bài tập | Đầu vào / Đầu ra chính |
|---|---|---|---|
| **Bài 1** | [`bai1.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai1.py) | Ghi và đọc file văn bản | `sentences.txt`, đếm dòng, câu dài nhất |
| **Bài 2** | [`bai2.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai2.py) | Đếm từ trong file | `story.txt` $\rightarrow$ `summary.txt` (Top 5 từ) |
| **Bài 3** | [`bai3.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai3.py) | Copy file lớn dùng Thread | `source.txt` $\rightarrow$ `target.txt`, hiển thị byte & tiến độ, so sánh thời gian, MD5 |
| **Bài 4** | [`bai4.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai4.py) | Tạo file logs đa luồng | 3 thread ghi 30 dòng vào `logs.txt` với `threading.Lock` |
| **Bài 5** | [`bai5.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai5.py) | Theo dõi file thay đổi bằng Thread | Theo dõi `watched.txt` mỗi 3s, luồng user ghi thêm, tự dừng sau 30s |
| **Bài 6** | [`bai6.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai6.py) | Ghi thông tin sinh viên vào JSON | Serialize/Deserialize `students.json` |
| **Bài 7** | [`bai7.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai7.py) | Quản lý task (ToDo) với JSON | `add_task()`, `load_tasks()`, xử lý `FileNotFoundError` & `JSONDecodeError` |
| **Bài 8** | [`bai8.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai8.py) | Sử dụng pickle lưu trạng thái đối tượng | `class GameState`, lưu `state.dat`, xác minh tính toàn vẹn |
| **Bài 9** | [`bai9.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai9.py) | Giao tiếp giữa hàm qua JSON | Hàm A (serialize) $\rightarrow$ Hàm B (deserialize, ép float, tính tiền 3 sp) |
| **Bài 10** | [`bai10.py`](file:///Users/duongnad/Documents/Aptech/Python/lab4/bai10.py) | Chuyển đổi CSV thành JSON | `products.csv` $\rightarrow$ `products.json` (đảm bảo Price là float) |

---

## 🚀 Hướng dẫn chạy

### 1. Chạy tất cả 10 bài cùng lúc
```bash
cd /Users/duongnad/Documents/Aptech/Python/lab4
python3 run_all.py
```

### 2. Chạy từng bài riêng biệt
```bash
# Ví dụ chạy bài 1:
python3 bai1.py

# Ví dụ chạy bài 2:
python3 bai2.py

# Ví dụ chạy bài 3 (Copy file lớn dùng Thread):
python3 bai3.py

# Ví dụ chạy bài 4 (Đa luồng ghi log với Lock):
python3 bai4.py

# Ví dụ chạy bài 5 (Theo dõi file 30 giây):
python3 bai5.py

# Hoặc dùng script run_all kèm số thứ tự bài:
python3 run_all.py 7   # Chạy Bài 7
```
