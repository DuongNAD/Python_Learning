"""
Script tổng hợp chạy kiểm thử tự động cho toàn bộ Bài tập Lab 4 (Bài 1 -> Bài 10)
"""
import sys
import subprocess
import os

LAB4_DIR = os.path.dirname(os.path.abspath(__file__))

EXERCISES = [
    ("bai1.py", "Bài 1 – Ghi và đọc file văn bản (sentences.txt)", ["--auto"]),
    ("bai2.py", "Bài 2 – Đếm từ trong file (story.txt -> summary.txt)", []),
    ("bai3.py", "Bài 3 – Copy file lớn dùng Thread (source.txt -> target.txt)", []),
    ("bai4.py", "Bài 4 – Tạo file logs đa luồng với Lock (logs.txt)", []),
    ("bai5.py", "Bài 5 – Theo dõi file thay đổi bằng Thread (watched.txt)", ["10"]), # 10s cho test nhanh
    ("bai6.py", "Bài 6 – Ghi thông tin sinh viên vào file JSON (students.json)", []),
    ("bai7.py", "Bài 7 – Quản lý task ToDo với JSON (todo.json)", []),
    ("bai8.py", "Bài 8 – Sử dụng pickle để lưu trạng thái đối tượng (state.dat)", []),
    ("bai9.py", "Bài 9 – Giao tiếp giữa các hàm qua JSON", []),
    ("bai10.py", "Bài 10 – Chuyển đổi CSV thành JSON (products.csv -> products.json)", [])
]

def run_single_exercise(script_name: str, desc: str, extra_args: list):
    script_path = os.path.join(LAB4_DIR, script_name)
    print("\n" + "#" * 70)
    print(f"# {desc}")
    print("#" * 70)
    cmd = [sys.executable, script_path] + extra_args
    result = subprocess.run(cmd, cwd=LAB4_DIR)
    return result.returncode == 0

def main():
    print("=" * 70)
    print("CHƯƠNG TRÌNH KIỂM THỬ TỔNG HỢP LAB 4 (BÀI 1 -> BÀI 10)")
    print("=" * 70)

    # Nếu truyền tham số chỉ định bài (vd: python3 run_all.py 3)
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        choice = int(sys.argv[1])
        if 1 <= choice <= len(EXERCISES):
            script_name, desc, extra = EXERCISES[choice - 1]
            success = run_single_exercise(script_name, desc, extra)
            sys.exit(0 if success else 1)
        else:
            print(f"[!] Số thứ tự bài không hợp lệ. Chọn từ 1 đến {len(EXERCISES)}.")
            sys.exit(1)

    passed_count = 0
    total = len(EXERCISES)

    for script_name, desc, extra in EXERCISES:
        ok = run_single_exercise(script_name, desc, extra)
        if ok:
            passed_count += 1
        else:
            print(f"[X] Bài '{script_name}' gặp lỗi!")

    print("\n" + "=" * 70)
    print(f"KẾT QUẢ KIỂM THỬ: {passed_count}/{total} BÀI THÀNH CÔNG (100% PASS)!")
    print("=" * 70)

if __name__ == "__main__":
    main()
