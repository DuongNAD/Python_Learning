import mysql.connector
from mysql.connector import errorcode
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from logger import logger

def get_db_connection(include_db: bool = True):
    """
    Tạo và trả về connection tới MySQL.
    Nếu include_db=False, kết nối tới server MySQL không chọn trước DB (dùng để tạo DB).
    """
    kwargs = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
    }
    if include_db:
        kwargs["database"] = DB_NAME

    try:
        conn = mysql.connector.connect(**kwargs)
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Lỗi kết nối MySQL: {err}")
        raise err

def init_db():
    """
    Hàm khởi tạo CSDL:
    1. Tự động tạo CSDL user_system nếu chưa tồn tại.
    2. Tự động tạo bảng users nếu chưa tồn tại với các trường:
       id, name, email, password, created_at.
    """
    try:
        # Bước 1: Kết nối server MySQL để tạo CSDL nếu chưa có
        conn = get_db_connection(include_db=False)
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        cursor.close()
        conn.close()
        logger.info(f"Đã đảm bảo CSDL '{DB_NAME}' tồn tại.")

        # Bước 2: Kết nối vào CSDL vừa tạo để tạo bảng users
        conn = get_db_connection(include_db=True)
        cursor = conn.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_table_sql)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Đã đảm bảo bảng 'users' tồn tại với cấu trúc đầy đủ.")
    except mysql.connector.Error as err:
        logger.error(f"Lỗi khi khởi tạo CSDL: {err}")
        raise err

if __name__ == "__main__":
    init_db()
    print("Khởi tạo CSDL hoàn tất!")
