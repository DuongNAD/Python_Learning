"""
Bài 2 – Đếm từ trong file
Yêu cầu:
- Cho sẵn file story.txt (tạo trước).
- Đọc nội dung file và đếm tổng số từ.
- In top 5 từ xuất hiện nhiều nhất.
- Bỏ qua dấu câu và không phân biệt chữ hoa thường.
- Ghi kết quả vào file summary.txt.
"""
import os
import re
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORY_FILE = os.path.join(BASE_DIR, "story.txt")
SUMMARY_FILE = os.path.join(BASE_DIR, "summary.txt")

def main():
    print("=" * 60)
    print("BÀI 2: ĐẾM TỪ TRONG FILE (story.txt -> summary.txt)")
    print("=" * 60)

    if not os.path.exists(STORY_FILE):
        print(f"[!] File {STORY_FILE} chưa tồn tại. Đang tạo file mặc định...")
        default_story = (
            "Python là ngôn ngữ lập trình tuyệt vời. Python đơn giản và Python rất mạnh mẽ.\n"
            "Lập trình viên yêu thích Python vì Python giúp tự động hoá công việc hiệu quả."
        )
        with open(STORY_FILE, "w", encoding="utf-8") as f:
            f.write(default_story)

    # 1. Đọc nội dung file story.txt
    with open(STORY_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"\n[+] Đã đọc nội dung từ file '{os.path.basename(STORY_FILE)}':")
    print("-" * 50)
    print(content.strip())
    print("-" * 50)

    # 2. Xử lý chuẩn hoá: Bỏ qua dấu câu và chuyển về chữ thường
    # Thay thế các dấu câu, ký tự đặc biệt bằng khoảng trắng
    clean_content = re.sub(r"[^\w\s]", " ", content)
    words = clean_content.lower().split()

    # 3. Đếm tổng số từ
    total_words = len(words)
    print(f"\n[+] Tổng số từ trong file: {total_words} từ")

    # 4. Tìm top 5 từ xuất hiện nhiều nhất
    word_counts = Counter(words)
    top_5 = word_counts.most_common(5)

    print("\n[+] Top 5 từ xuất hiện nhiều nhất:")
    for rank, (word, count) in enumerate(top_5, 1):
        print(f"    {rank}. '{word}': {count} lần")

    # 5. Ghi kết quả vào file summary.txt
    summary_content = [
        "========================================",
        "BÁO CÁO THỐNG KÊ TỪ TRONG STORY.TXT",
        "========================================",
        f"Tổng số từ: {total_words}",
        f"Số lượng từ vựng độc nhất: {len(word_counts)}",
        "",
        "TOP 5 TỪ XUẤT HIỆN NHIỀU NHẤT:",
    ]
    for rank, (word, count) in enumerate(top_5, 1):
        percentage = (count / total_words) * 100 if total_words > 0 else 0
        summary_content.append(f"{rank}. {word}: {count} lần ({percentage:.1f}%)")

    summary_text = "\n".join(summary_content)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write(summary_text + "\n")

    print(f"\n[+] Đã ghi toàn bộ kết quả thống kê vào file: '{os.path.basename(SUMMARY_FILE)}'")

if __name__ == "__main__":
    main()
