import os
from dotenv import load_dotenv

# Nạp các biến môi trường từ .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "user_system")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
LOG_FILE = os.getenv("LOG_FILE", "app.log")
