from database import init_db, get_db_connection
from auth import hash_password
from logger import logger, log_action
from crud import get_user_by_email

SAMPLE_USERS = [
    {
        "name": "Nguyễn Văn An",
        "email": "nguyenvanan@example.com",
        "password": "Password123@",
    },
    {
        "name": "Trần Thị Bích",
        "email": "tranthibich@example.com",
        "password": "Password123@",
    },
    {
        "name": "Lê Hoàng Cường",
        "email": "lehoangcuong@example.com",
        "password": "Password123@",
    },
    {
        "name": "Phạm Minh Dung",
        "email": "phamminhdung@example.com",
        "password": "Password123@",
    },
    {
        "name": "Hoàng Quốc Em",
        "email": "hoangquocem@example.com",
        "password": "Password123@",
    }
]

def seed_sample_data():
    """
    Thêm 5 người dùng mẫu vào CSDL để test theo yêu cầu Lab 6
    """
    # Đảm bảo CSDL và bảng đã tồn tại
    init_db()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        inserted_count = 0
        print("=" * 60)
        print("Đang khởi tạo dữ liệu mẫu (5 người dùng)...")
        print("=" * 60)

        for user in SAMPLE_USERS:
            # Kiểm tra xem email đã tồn tại hay chưa
            existing = get_user_by_email(user["email"])
            if not existing:
                hashed = hash_password(user["password"])
                cursor.execute(
                    "INSERT INTO users (name, email, password, created_at) VALUES (%s, %s, %s, NOW())",
                    (user["name"], user["email"], hashed)
                )
                conn.commit()
                new_id = cursor.lastrowid
                inserted_count += 1
                log_action("THÊM", f"[Init Data] Thêm người dùng mẫu: ID={new_id}, Name='{user['name']}', Email='{user['email']}'")
                print(f" [+] Đã thêm: ID={new_id} | {user['name']} | {user['email']}")
            else:
                print(f" [=] Đã tồn tại: {user['email']} (bỏ qua)")

        print("=" * 60)
        print(f"Hoàn thành! Đã thêm mới {inserted_count} người dùng mẫu vào MySQL.")
        print("=" * 60)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_sample_data()
