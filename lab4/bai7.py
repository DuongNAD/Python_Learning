"""
Bài 7 – Quản lý task (ToDo) với JSON
Yêu cầu:
- Tạo hàm add_task() thêm task vào list.
- Serialize list task vào file todo.json.
- Tạo hàm load_tasks() đọc lại từ file.
- In các task từ file lên console.
- Bắt lỗi khi file không tồn tại hoặc bị lỗi định dạng.
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TODO_FILE = os.path.join(BASE_DIR, "todo.json")

def add_task(tasks: List[Dict[str, Any]], title: str, priority: str = "Medium", completed: bool = False) -> Dict[str, Any]:
    """Hàm thêm một task mới vào danh sách task"""
    new_id = len(tasks) + 1
    new_task = {
        "id": new_id,
        "title": title,
        "priority": priority,
        "completed": completed,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    return new_task

def save_tasks(tasks: List[Dict[str, Any]], file_path: str = TODO_FILE):
    """Serialize danh sách task vào file JSON"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
        print(f"[+] Đã lưu {len(tasks)} task vào file '{os.path.basename(file_path)}'")
    except Exception as e:
        print(f"[!] Lỗi khi ghi file '{file_path}': {e}")

def load_tasks(file_path: str = TODO_FILE) -> List[Dict[str, Any]]:
    """
    Đọc lại danh sách task từ file JSON.
    Bắt lỗi khi file không tồn tại hoặc bị lỗi định dạng.
    """
    if not os.path.exists(file_path):
        print(f"[WARN] File '{os.path.basename(file_path)}' không tồn tại (FileNotFoundError). Khởi tạo danh sách rỗng.")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            if not isinstance(tasks, list):
                print(f"[WARN] Dữ liệu trong file '{os.path.basename(file_path)}' không phải là một danh sách hợp lệ.")
                return []
            return tasks
    except json.JSONDecodeError as decode_err:
        print(f"[ERROR] Lỗi định dạng JSON trong file '{os.path.basename(file_path)}': {decode_err}")
        return []
    except Exception as e:
        print(f"[ERROR] Lỗi không xác định khi nạp task: {e}")
        return []

def print_tasks(tasks: List[Dict[str, Any]]):
    """In danh sách task lên console một cách trực quan"""
    print("\n--- DANH SÁCH CÔNG VIỆC (TODO LIST) ---")
    if not tasks:
        print(" (Danh sách hiện đang trống)")
        return

    print(f"{'ID':<4} | {'Trạng thái':<12} | {'Ưu tiên':<10} | {'Tiêu đề công việc':<35} | {'Thời gian tạo'}")
    print("-" * 85)
    for t in tasks:
        status_str = "[x] Đã xong" if t.get("completed") else "[ ] Chưa xong"
        print(f"{t.get('id', '-'):<4} | {status_str:<12} | {t.get('priority', 'Normal'):<10} | {t.get('title', ''):<35} | {t.get('created_at', '')}")
    print("-" * 85)

def main():
    print("=" * 60)
    print("BÀI 7: QUẢN LÝ TASK (TODO) VỚI FILE JSON")
    print("=" * 60)

    # 1. Thử nghiệm bắt lỗi File không tồn tại
    non_existent = os.path.join(BASE_DIR, "non_existent_todo.json")
    print("\n[1] Kiểm thử bắt lỗi khi file KHÔNG tồn tại:")
    result = load_tasks(non_existent)
    print(f"    Kết quả trả về an toàn: {result}")

    # 2. Thử nghiệm bắt lỗi File bị hỏng định dạng JSON
    corrupted_file = os.path.join(BASE_DIR, "corrupted_todo.json")
    with open(corrupted_file, "w", encoding="utf-8") as f:
        f.write("{ invalid json format... [ ")
    print("\n[2] Kiểm thử bắt lỗi khi file BỊ LỖI ĐỊNH DẠNG JSON:")
    result = load_tasks(corrupted_file)
    print(f"    Kết quả trả về an toàn: {result}")
    if os.path.exists(corrupted_file):
        os.remove(corrupted_file)

    # 3. Thao tác chính: Thêm task bằng hàm add_task()
    print("\n[3] Thêm các task vào danh sách bằng hàm add_task():")
    my_tasks = []
    add_task(my_tasks, "Ôn tập kiến thức Python File & JSON", priority="High", completed=True)
    add_task(my_tasks, "Làm bài tập Lab 4 (Bài 1 -> Bài 10)", priority="High", completed=True)
    add_task(my_tasks, "Thực hành Threading trong Python", priority="Medium", completed=False)
    add_task(my_tasks, "Xây dựng ứng dụng FastAPI và Jinja2", priority="High", completed=False)
    add_task(my_tasks, "Nghiên cứu mô hình YOLOv8 Object Detection", priority="Low", completed=False)

    for t in my_tasks:
        print(f" [+] Đã thêm: #{t['id']} - {t['title']} ({t['priority']})")

    # 4. Serialize list task vào file todo.json
    print(f"\n[4] Lưu vào file '{os.path.basename(TODO_FILE)}':")
    save_tasks(my_tasks, TODO_FILE)

    # 5. Gọi hàm load_tasks() đọc lại từ file và in lên console
    print(f"\n[5] Nạp lại task từ file và in ra console:")
    loaded = load_tasks(TODO_FILE)
    print_tasks(loaded)

    print("\n[PASS] BÀI 7 HOÀN THÀNH XUẤT SẮC ĐẦY ĐỦ CÁC YÊU CẦU!")

if __name__ == "__main__":
    main()
