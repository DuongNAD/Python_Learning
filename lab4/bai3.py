"""
Bài 3 – Copy file lớn dùng Thread
Yêu cầu:
- Viết chương trình sao chép file source.txt thành target.txt.
- Dùng thread để xử lý việc copy file.
- Hiển thị tiến độ (số byte đã copy).
- So sánh thời gian copy với/không dùng thread.
- Đảm bảo file đích giống file gốc (xác minh MD5 checksum).
"""
import os
import time
import hashlib
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(BASE_DIR, "source.txt")
TARGET_FILE = os.path.join(BASE_DIR, "target.txt")
DIRECT_TARGET = os.path.join(BASE_DIR, "target_direct.txt")
CHUNK_SIZE = 1024 * 64  # 64 KB mỗi chunk

def generate_large_source_file(file_path: str, size_in_mb: int = 5):
    """Tạo file lớn source.txt để thực hiện kiểm thử sao chép"""
    print(f"[*] Đang chuẩn bị file nguồn '{os.path.basename(file_path)}' (~{size_in_mb} MB)...")
    pattern = ("Dữ liệu thử nghiệm sao chép đa luồng bằng Python trong Lab 4 Aptech. " * 5).encode("utf-8")
    bytes_written = 0
    target_bytes = size_in_mb * 1024 * 1024
    with open(file_path, "wb") as f:
        while bytes_written < target_bytes:
            f.write(pattern)
            bytes_written += len(pattern)
    print(f"[+] Đã tạo file '{os.path.basename(file_path)}' ({bytes_written / (1024*1024):.2f} MB)")

def compute_md5(file_path: str) -> str:
    """Tính toán mã băm MD5 để xác minh tính toàn vẹn của file"""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

def copy_direct(src: str, dst: str):
    """Sao chép tuần tự thông thường (không dùng thread)"""
    start_time = time.time()
    with open(src, "rb") as f_in, open(dst, "wb") as f_out:
        while chunk := f_in.read(CHUNK_SIZE):
            f_out.write(chunk)
    elapsed = time.time() - start_time
    return elapsed

class ThreadedCopier:
    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst
        self.total_size = os.path.getsize(src)
        self.copied_bytes = 0
        self.is_done = False
        self.error = None

    def _worker(self):
        try:
            with open(self.src, "rb") as f_in, open(self.dst, "wb") as f_out:
                while chunk := f_in.read(CHUNK_SIZE):
                    f_out.write(chunk)
                    self.copied_bytes += len(chunk)
        except Exception as e:
            self.error = e
        finally:
            self.is_done = True

    def run(self):
        start_time = time.time()
        thread = threading.Thread(target=self._worker, name="CopyWorker")
        thread.start()

        # Hiển thị tiến độ từ luồng chính
        print("\n--- TIẾN ĐỘ SAO CHÉP VỚI THREAD ---")
        while not self.is_done or thread.is_alive():
            progress = (self.copied_bytes / self.total_size) * 100 if self.total_size > 0 else 0
            mb_copied = self.copied_bytes / (1024 * 1024)
            mb_total = self.total_size / (1024 * 1024)
            print(f"\rTiến độ: {progress:6.2f}% | Đã copy: {mb_copied:.2f} MB / {mb_total:.2f} MB ({self.copied_bytes} bytes)", end="", flush=True)
            time.sleep(0.05)

        thread.join()
        print(f"\rTiến độ: 100.00% | Đã copy: {self.total_size / (1024*1024):.2f} MB / {self.total_size / (1024*1024):.2f} MB ({self.total_size} bytes)")
        elapsed = time.time() - start_time

        if self.error:
            raise self.error
        return elapsed

def main():
    print("=" * 60)
    print("BÀI 3: SAO CHÉP FILE LỚN DÙNG THREAD (source.txt -> target.txt)")
    print("=" * 60)

    # 1. Đảm bảo file nguồn tồn tại
    if not os.path.exists(SOURCE_FILE) or os.path.getsize(SOURCE_FILE) < 1024 * 1024:
        generate_large_source_file(SOURCE_FILE, size_in_mb=6)

    source_size = os.path.getsize(SOURCE_FILE)
    print(f"\n[+] File nguồn: '{os.path.basename(SOURCE_FILE)}' ({source_size / (1024*1024):.2f} MB)")

    # 2. Sao chép KHÔNG dùng thread
    print("\n[1] Thực hiện sao chép KHÔNG dùng thread (Direct Copy)...")
    time_without_thread = copy_direct(SOURCE_FILE, DIRECT_TARGET)
    print(f"[+] Hoàn tất! Thời gian: {time_without_thread:.4f} giây")

    # 3. Sao chép DÙNG thread có hiển thị tiến độ
    print("\n[2] Thực hiện sao chép DÙNG thread (Threaded Copy)...")
    copier = ThreadedCopier(SOURCE_FILE, TARGET_FILE)
    time_with_thread = copier.run()
    print(f"[+] Hoàn tất! Thời gian: {time_with_thread:.4f} giây")

    # 4. So sánh thời gian
    print("\n" + "=" * 50)
    print("BẢNG SO SÁNH THỜI GIAN SAO CHÉP")
    print("=" * 50)
    print(f" - Không dùng thread: {time_without_thread:.4f} giây")
    print(f" - Dùng thread:        {time_with_thread:.4f} giây")
    diff = abs(time_with_thread - time_without_thread)
    print(f" -> Chênh lệch:        {diff:.4f} giây")
    print("   (Ghi chú: Luồng sao chép chạy nền giúp chương trình không bị block giao diện)")

    # 5. Đảm bảo file đích giống hệt file gốc
    print("\n--- KIỂM TRA TÍNH TOÀN VẸN CỦA FILE (MD5 CHECKSUM) ---")
    source_md5 = compute_md5(SOURCE_FILE)
    target_md5 = compute_md5(TARGET_FILE)
    print(f"MD5 File gốc:  {source_md5}")
    print(f"MD5 File đích: {target_md5}")

    if source_md5 == target_md5:
        print("[PASS] XÁC NHẬN: File đích GIỐNG HỆT file gốc 100%!")
    else:
        print("[FAIL] CẢNH BÁO: Dữ liệu file đích không trùng khớp!")

if __name__ == "__main__":
    main()
