"""
Bài 10 – Chuyển đổi CSV thành JSON
Yêu cầu:
- Tạo file products.csv chứa danh sách sản phẩm (Name, Price).
- Đọc file CSV thành list of dict.
- Serialize thành file products.json.
- In nội dung JSON.
- Đảm bảo giá là số (float), không phải chuỗi.
"""
import os
import csv
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "products.csv")
JSON_FILE = os.path.join(BASE_DIR, "products.json")

def create_sample_csv():
    """Tạo file products.csv mẫu chứa Name và Price"""
    sample_data = [
        ["Name", "Price"],
        ["Chuột không dây Logitech", "450000"],
        ["Bàn phím cơ Keychron K2", "1850000.50"],
        ["Tai nghe chống ồn Sony WH-1000XM5", "6990000"],
        ["Màn hình Dell UltraSharp 27 inch", "9200000.75"],
        ["Đế tản nhiệt Laptop nhôm", "320000"]
    ]
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    print(f"[+] Đã tạo file '{os.path.basename(CSV_FILE)}' mẫu thành công.")

def convert_csv_to_json():
    """Đọc file CSV, chuyển đổi dữ liệu và xuất sang products.json"""
    # 1. Đọc file CSV thành list of dict
    products_list = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Đảm bảo trường Price là kiểu float, không phải chuỗi (str)
            try:
                price_val = float(row["Price"].strip())
            except ValueError:
                price_val = 0.0

            product_entry = {
                "Name": row["Name"].strip(),
                "Price": price_val
            }
            products_list.append(product_entry)

    # 2. Serialize thành file products.json
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(products_list, f, ensure_ascii=False, indent=4)
    print(f"[+] Đã chuyển đổi và lưu {len(products_list)} sản phẩm vào '{os.path.basename(JSON_FILE)}'")

    # 3. Đọc lại và in nội dung JSON
    print("\n--- NỘI DUNG FILE PRODUCTS.JSON ---")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        json_content_str = f.read()
    print(json_content_str)

    # 4. Kiểm tra đảm bảo kiểu dữ liệu là float
    loaded_data = json.loads(json_content_str)
    all_prices_are_float = all(isinstance(item["Price"], (float, int)) for item in loaded_data)
    print("\n--- KIỂM TRA ĐỊNH DẠNG DỮ LIỆU ---")
    for item in loaded_data:
        val = item["Price"]
        print(f" - {item['Name']}: {val} -> Kiểu dữ liệu: {type(val).__name__}")

    if all_prices_are_float:
        print("\n[PASS] XÁC NHẬN: Mọi trường Price đều là số (float/int), không phải chuỗi ký tự!")
    else:
        print("\n[FAIL] Có trường Price vẫn là chuỗi!")

def main():
    print("=" * 60)
    print("BÀI 10: CHUYỂN ĐỔI FILE CSV THÀNH JSON (products.csv -> products.json)")
    print("=" * 60)

    # 1. Tạo file products.csv
    create_sample_csv()

    # 2. Chuyển đổi sang products.json và in kết quả
    convert_csv_to_json()

if __name__ == "__main__":
    main()
