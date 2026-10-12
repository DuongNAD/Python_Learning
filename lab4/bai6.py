"""
Bài 6 – Ghi thông tin sinh viên vào file JSON
Yêu cầu:
- Tạo danh sách các sinh viên (dict).
- Serialize danh sách thành JSON.
- Ghi JSON vào file students.json.
- Đọc file và deserialize thành lại danh sách.
- In danh sách đã đọc ra màn hình.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(BASE_DIR, "students.json")

def main():
    print("=" * 60)
    print("BÀI 6: GHI VÀ ĐỌC THÔNG TIN SINH VIÊN VỚI JSON")
    print("=" * 60)

    # 1. Tạo danh sách các sinh viên (list of dict)
    students = [
        {"id": "SV001", "name": "Nguyễn Văn An", "age": 20, "major": "Công nghệ thông tin", "gpa": 3.65},
        {"id": "SV002", "name": "Trần Thị Bích", "age": 21, "major": "Khoa học máy tính", "gpa": 3.82},
        {"id": "SV003", "name": "Lê Hoàng Cường", "age": 20, "major": "Kỹ thuật phần mềm", "gpa": 3.45},
        {"id": "SV004", "name": "Phạm Minh Dung", "age": 22, "major": "Hệ thống thông tin", "gpa": 3.90},
        {"id": "SV005", "name": "Vũ Hải Đăng", "age": 21, "major": "An toàn thông tin", "gpa": 3.55}
    ]

    print(f"\n[1] Danh sách sinh viên ban đầu ({len(students)} sinh viên):")
    for s in students:
        print(f" - [{s['id']}] {s['name']} | Tuổi: {s['age']} | Chuyên ngành: {s['major']} | GPA: {s['gpa']}")

    # 2. Serialize danh sách thành JSON và ghi vào file students.json
    print(f"\n[2] Đang serialize và ghi vào file '{os.path.basename(STUDENTS_FILE)}'...")
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=4)
    print(f"[+] Ghi file thành công!")

    # 3. Đọc file và deserialize lại thành danh sách đối tượng
    print(f"\n[3] Đang đọc file và deserialize từ '{os.path.basename(STUDENTS_FILE)}'...")
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        loaded_students = json.load(f)

    # 4. In danh sách đã đọc ra màn hình
    print("\n--- DANH SÁCH SINH VIÊN SAU KHI DESERIALIZE ---")
    print(f"{'Mã SV':<8} | {'Họ và Tên':<20} | {'Tuổi':<6} | {'Chuyên ngành':<22} | {'GPA':<5}")
    print("-" * 72)
    for s in loaded_students:
        print(f"{s['id']:<8} | {s['name']:<20} | {s['age']:<6} | {s['major']:<22} | {s['gpa']:<5.2f}")
    print("-" * 72)

    # 5. Kiểm tra tính toàn vẹn
    assert students == loaded_students, "Dữ liệu sau khi deserialize không khớp!"
    print("\n[PASS] Dữ liệu đọc lại hoàn toàn khớp chính xác với dữ liệu ban đầu!")

if __name__ == "__main__":
    main()
