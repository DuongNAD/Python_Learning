"""
Bài 1 – Ghi và đọc file văn bản
Yêu cầu:
- Nhập vào 5 câu bất kỳ từ bàn phím.
- Ghi các câu này vào file sentences.txt.
- Đọc lại toàn bộ nội dung file và in ra.
- In tổng số dòng trong file.
- In câu dài nhất trong file.
"""
import os
import sys

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sentences.txt")

def main():
    print("=" * 60)
    print("BÀI 1: GHI VÀ ĐỌC FILE VĂN BẢN (sentences.txt)")
    print("=" * 60)

    sentences = []
    # Tự động nạp mẫu nếu có cờ --auto hoặc không phải terminal tương tác
    if "--auto" in sys.argv or not sys.stdin.isatty():
        sentences = [
            "Python là ngôn ngữ lập trình phổ biến và dễ học.",
            "FastAPI cung cấp hiệu năng cao tương đương NodeJS và Go.",
            "Trí tuệ nhân tạo và học máy đang phát triển với tốc độ chóng mặt.",
            "Học lập trình đòi hỏi sự kiên nhẫn, thực hành liên tục và tư duy phản biện sắc bén.",
            "Chúc bạn có một buổi học Python thật nhiều niềm vui và hiệu quả!"
        ]
        print("Đang tự động nạp 5 câu mẫu vào chương trình (chế độ tự động):")
        for idx, s in enumerate(sentences, 1):
            print(f" {idx}. {s}")
    else:
        print("Vui lòng nhập vào 5 câu bất kỳ:")
        for i in range(1, 6):
            while True:
                line = input(f"Nhập câu {i}/5: ").strip()
                if line:
                    sentences.append(line)
                    break
                print("Câu không được để trống! Vui lòng nhập lại.")

    # 1. Ghi 5 câu vào file sentences.txt
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for s in sentences:
            f.write(s + "\n")
    print(f"\n[+] Đã ghi thành công 5 câu vào file: '{os.path.basename(FILE_NAME)}'")

    # 2. Đọc lại toàn bộ nội dung file và in ra
    print("\n--- ĐỌC LẠI NỘI DUNG TỪ FILE ---")
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    for idx, line in enumerate(lines, 1):
        print(f"Dòng {idx}: {line}")

    # 3. In tổng số dòng trong file
    total_lines = len(lines)
    print(f"\n[+] Tổng số dòng trong file: {total_lines}")

    # 4. In câu dài nhất trong file
    if lines:
        longest_sentence = max(lines, key=len)
        print(f"[+] Câu dài nhất trong file ({len(longest_sentence)} ký tự):")
        print(f"    \"{longest_sentence}\"")

if __name__ == "__main__":
    main()
