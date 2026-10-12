"""
Bài 9 – Giao tiếp giữa hàm qua JSON
Yêu cầu:
- Hàm A tạo dictionary product và serialize sang JSON string.
- Hàm B nhận JSON string, deserialize thành dict.
- Hàm B in tên sản phẩm và giá.
- Chuyển đổi giá tiền sang float.
- In tổng số tiền nếu số lượng là 3 sản phẩm.
"""
import json

def function_A() -> str:
    """
    Hàm A: Tạo dictionary product và serialize sang chuỗi JSON string
    """
    product = {
        "id": "SP-8899",
        "name": "Bàn phím cơ Gaming không dây RGB",
        "price": "1450000",  # Giá ban đầu có thể là chuỗi số
        "currency": "VND",
        "in_stock": True,
        "manufacturer": "TechMaster"
    }
    # Serialize dictionary thành JSON string
    json_string = json.dumps(product, ensure_ascii=False, indent=2)
    print("--- [HÀM A] ---")
    print("Đã tạo dictionary sản phẩm và serialize sang chuỗi JSON:")
    print(json_string)
    return json_string

def function_B(json_string: str, quantity: int = 3):
    """
    Hàm B: Nhận JSON string, deserialize thành dict,
    chuyển đổi giá sang float và tính tổng tiền cho số lượng chỉ định (3 sản phẩm)
    """
    print("\n--- [HÀM B] ---")
    print("Đang nhận và deserialize chuỗi JSON...")
    # Deserialize JSON string thành Python dictionary
    product = json.loads(json_string)

    # Lấy thông tin tên sản phẩm
    product_name = product.get("name", "Không rõ")
    raw_price = product.get("price", 0)

    # Chuyển đổi giá tiền sang float theo yêu cầu
    price_float = float(raw_price)
    currency = product.get("currency", "VND")

    print(f"[+] Tên sản phẩm: {product_name}")
    print(f"[+] Đơn giá gốc:  {price_float:,.2f} {currency} (Kiểu dữ liệu: {type(price_float).__name__})")

    # Tính và in tổng số tiền nếu số lượng là 3 sản phẩm
    total_amount = price_float * quantity
    print(f"\n[+] Số lượng mua: {quantity} sản phẩm")
    print(f"[+] TỔNG SỐ TIỀN THANH TOÁN: {total_amount:,.2f} {currency}")

def main():
    print("=" * 60)
    print("BÀI 9: GIAO TIẾP GIỮA CÁC HÀM QUA ĐỊNH DẠNG JSON")
    print("=" * 60)

    # Hàm A tạo JSON string
    data_packet = function_A()

    # Truyền JSON string vào Hàm B để xử lý
    function_B(data_packet, quantity=3)

    print("\n[PASS] BÀI 9 HOÀN THÀNH XUẤT SẮC!")

if __name__ == "__main__":
    main()
