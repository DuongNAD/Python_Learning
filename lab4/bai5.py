"""
Bài 5 – Theo dõi file thay đổi bằng thread
Yêu cầu:
- Viết hàm theo dõi file watched.txt.
- Cứ 3 giây kiểm tra lại nội dung file.
- Nếu nội dung thay đổi thì in dòng mới.
- Cho phép ghi vào file từ thread khác (giả lập user).
- Sau 30 giây tự động dừng chương trình.
"""
import os
import time
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WATCHED_FILE = os.path.join(BASE_DIR, "watched.txt")

stop_event = threading.Event()
file_write_lock = threading.Lock()

def file_watcher(file_path: str, check_interval: int = 3):
    """Luồng theo dõi: Cứ mỗi check_interval (3 giây) kiểm tra nội dung file một lần"""
    print(f"[Watcher] Đã khởi động luồng theo dõi file '{os.path.basename(file_path)}' (Chu kỳ {check_interval}s)")
    last_lines = []

    # Đọc trạng thái ban đầu nếu file đã có nội dung
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            last_lines = [line.strip() for line in f.readlines() if line.strip()]

    while not stop_event.is_set():
        # Chờ 3 giây (có thể bị ngắt sớm nếu stop_event kích hoạt)
        if stop_event.wait(timeout=check_interval):
            break

        if os.path.exists(file_path):
            with file_write_lock:
                with open(file_path, "r", encoding="utf-8") as f:
                    current_lines = [line.strip() for line in f.readlines() if line.strip()]

            # So sánh và tìm các dòng mới được thêm vào
            if len(current_lines) > len(last_lines):
                new_items = current_lines[len(last_lines):]
                print(f"\n🔔 [Watcher - {time.strftime('%H:%M:%S')}] Phát hiện {len(new_items)} dòng mới:")
                for item in new_items:
                    print(f"   --> {item}")
                last_lines = current_lines
            elif current_lines != last_lines:
                print(f"\n🔔 [Watcher - {time.strftime('%H:%M:%S')}] File đã được chỉnh sửa nội dung!")
                last_lines = current_lines

    print("[Watcher] Luồng theo dõi đã dừng an toàn.")

def user_simulator(file_path: str):
    """Luồng giả lập người dùng ghi dữ liệu ngẫu nhiên vào file watched.txt"""
    sample_messages = [
        "Người dùng vừa đăng nhập vào hệ thống.",
        "Cập nhật trạng thái đơn hàng #1002 thành Đang giao.",
        "Người dùng đã thay đổi ảnh đại diện cá nhân.",
        "Phát hiện kết nối mới từ địa chỉ IP 192.168.1.105.",
        "Người dùng đã hoàn thành bài tập Lab 4 thành công!"
    ]

    print("[UserSimulator] Luồng giả lập người dùng bắt đầu hoạt động...")
    msg_idx = 0

    while not stop_event.is_set() and msg_idx < len(sample_messages):
        # Chờ khoảng 5-6 giây giữa các lần ghi
        if stop_event.wait(timeout=5):
            break

        msg = sample_messages[msg_idx]
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {msg}\n"

        with file_write_lock:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(entry)
                f.flush()

        print(f"✍️  [UserSimulator - {timestamp}] Đã ghi dòng {msg_idx + 1}: \"{msg}\"")
        msg_idx += 1

    print("[UserSimulator] Luồng người dùng đã hoàn thành việc ghi.")

def main(total_duration: int = 30):
    print("=" * 60)
    print("BÀI 5: THEO DÕI FILE THAY ĐỔI BẰNG THREAD (watched.txt)")
    print(f"Chương trình sẽ tự động dừng sau {total_duration} giây theo yêu cầu đề bài.")
    print("=" * 60)

    # Khởi tạo lại file rỗng ban đầu
    with open(WATCHED_FILE, "w", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] Khởi tạo file theo dõi ban đầu.\n")

    # Khởi tạo 2 thread
    t_watcher = threading.Thread(target=file_watcher, args=(WATCHED_FILE, 3), name="WatcherThread")
    t_user = threading.Thread(target=user_simulator, args=(WATCHED_FILE,), name="UserThread")

    start_time = time.time()
    t_watcher.start()
    t_user.start()

    # Đồng hồ đếm ngược 30 giây trong luồng chính
    try:
        while time.time() - start_time < total_duration:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Nhận tín hiệu dừng từ bàn phím (Ctrl+C).")

    print(f"\n[+] Đã đủ {total_duration} giây. Đang gửi tín hiệu dừng chương trình...")
    stop_event.set()

    t_watcher.join(timeout=5)
    t_user.join(timeout=5)

    print("\n--- TOÀN BỘ NỘI DUNG FILE WATCHED.TXT KHI KẾT THÚC ---")
    with open(WATCHED_FILE, "r", encoding="utf-8") as f:
        print(f.read().strip())

    print("\n[PASS] CHƯƠNG TRÌNH HOÀN THÀNH VÀ DỪNG ĐÚNG THEO YÊU CẦU!")

if __name__ == "__main__":
    import sys
    # Cho phép test nhanh với tham số thời gian (ví dụ: python3 bai5.py 10)
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    main(total_duration=duration)
