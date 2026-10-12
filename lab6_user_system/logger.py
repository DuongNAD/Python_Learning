import logging
import os
from config import LOG_FILE

# Thiết lập Logger ghi vào file app.log và in ra màn hình console
logger = logging.getLogger("user_system")
logger.setLevel(logging.INFO)

# Tránh add nhiều handler nếu file được import lại
if not logger.handlers:
    # Handler ghi vào file
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Handler ghi ra console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "[%(levelname)s] %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

def log_action(action: str, details: str):
    """
    Ghi log các thao tác THÊM / SỬA / XOÁ người dùng theo yêu cầu bài toán
    """
    logger.info(f"[{action.upper()}] {details}")
