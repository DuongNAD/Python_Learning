from typing import List, Optional, Dict, Any
from datetime import datetime
from database import get_db_connection
from logger import logger, log_action

def format_datetime(dt) -> str:
    """Định dạng thời gian theo yêu cầu: DD/MM/YYYY HH:MM"""
    if isinstance(dt, datetime):
        return dt.strftime("%d/%m/%Y %H:%M")
    elif dt:
        try:
            parsed = datetime.fromisoformat(str(dt))
            return parsed.strftime("%d/%m/%Y %H:%M")
        except Exception:
            return str(dt)
    return ""

def get_all_users() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY id DESC")
        rows = cursor.fetchall()
        for row in rows:
            row["created_at_raw"] = row["created_at"]
            row["created_at"] = format_datetime(row["created_at"])
        return rows
    finally:
        cursor.close()
        conn.close()

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            row["created_at_raw"] = row["created_at"]
            row["created_at"] = format_datetime(row["created_at"])
        return row
    finally:
        cursor.close()
        conn.close()

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name, email, password, created_at FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            row["created_at_raw"] = row["created_at"]
            row["created_at"] = format_datetime(row["created_at"])
        return row
    finally:
        cursor.close()
        conn.close()

def create_user(name: str, email: str, hashed_password: str) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, created_at) VALUES (%s, %s, %s, NOW())",
            (name, email, hashed_password)
        )
        conn.commit()
        new_id = cursor.lastrowid
        log_action("THÊM", f"Người dùng mới ID={new_id}, Name='{name}', Email='{email}'")
        return get_user_by_id(new_id)
    finally:
        cursor.close()
        conn.close()

def update_user(user_id: int, name: str, email: str, hashed_password: Optional[str] = None) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if hashed_password:
            cursor.execute(
                "UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s",
                (name, email, hashed_password, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET name = %s, email = %s WHERE id = %s",
                (name, email, user_id)
            )
        conn.commit()
        log_action("SỬA", f"Cập nhật người dùng ID={user_id}, Name='{name}', Email='{email}'")
        return get_user_by_id(user_id)
    finally:
        cursor.close()
        conn.close()

def delete_user(user_id: int) -> bool:
    user = get_user_by_id(user_id)
    if not user:
        return False
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        log_action("XOÁ", f"Xoá người dùng ID={user_id}, Name='{user['name']}', Email='{user['email']}'")
        return True
    finally:
        cursor.close()
        conn.close()
