"""
Bài 4 – Tạo file logs đa luồng
Yêu cầu:
- Tạo 3 thread, mỗi thread ghi log vào file logs.txt.
- Mỗi thread ghi 10 dòng như: Thread-1: log 1, ...
- Dùng threading.Lock để tránh ghi chồng dữ liệu.
- Đảm bảo toàn bộ log không bị lặp, thiếu hoặc ghi sai.
- Đọc file và xác nhận đúng 30 dòng.
"""
import os
import time
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")

file_lock = threading.Lock()

def worker_task(thread_name: str, num_logs: int = 10):
    """Công việc của mỗi thread: Ghi log vào file với lock an toàn"""
    for i in range(1, num_logs + 1):
        log_line = f"{thread_name}: log {i}\n"
        
        # Sử dụng threading.Lock để đồng bộ hoá ghi file
        with file_lock:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
                f.flush()
        
        # Giả lập thời gian xử lý nhỏ để các luồng xen kẽ nhau tự nhiên
        time.sleep(0.01)

def main():
    print("=" * 60)
    print("BÀI 4: TẠO FILE LOGS ĐA LUỒNG VỚI THREADING.LOCK")
    print("=" * 60)

    # 1. Reset file logs.txt trước khi ghi
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        pass
    print(f"[+] Đã làm mới file '{os.path.basename(LOG_FILE)}'")

    # 2. Khởi tạo 3 thread
    threads = []
    num_threads = 3
    logs_per_thread = 10

    for i in range(1, num_threads + 1):
        name = f"Thread-{i}"
        t = threading.Thread(target=worker_task, args=(name, logs_per_thread), name=name)
        threads.append(t)

    # 3. Chạy các thread
    print(f"\n[*] Đang khởi chạy {num_threads} thread...")
    start_time = time.time()
    for t in threads:
        t.start()
        print(f" [->] Khởi chạy {t.name}")

    # Chờ tất cả thread hoàn thành
    for t in threads:
        t.join()
    print(f"[+] Tất cả thread đã kết thúc trong {time.time() - start_time:.4f} giây.")

    # 4. Đọc file và kiểm tra xác nhận
    print("\n--- NỘI DUNG FILE LOGS.TXT ---")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    for idx, line in enumerate(lines, 1):
        print(f"{idx:2d}. {line}")

    # 5. Xác minh yêu cầu
    print("\n--- KẾT QUẢ KIỂM TRA & XÁC NHẬN ---")
    total_lines = len(lines)
    print(f"Tổng số dòng ghi được: {total_lines}/30 dòng")

    # Kiểm tra tính toàn vẹn của từng thread
    thread_counts = {}
    for line in lines:
        t_name = line.split(":")[0].strip()
        thread_counts[t_name] = thread_counts.get(t_name, 0) + 1

    for t_name, count in thread_counts.items():
        print(f" - {t_name}: {count}/10 dòng")

    if total_lines == 30 and all(c == 10 for c in thread_counts.values()):
        print("\n[PASS] XÁC NHẬN THÀNH CÔNG: Đúng 30 dòng, không bị lặp, thiếu hoặc ghi sai!")
    else:
        print("\n[FAIL] Số lượng dòng không đúng yêu cầu!")

if __name__ == "__main__":
    main()
