import os
from contextlib import asynccontextmanager
from typing import List, Optional
from urllib.parse import quote

from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import APP_PORT
from database import init_db
from auth import hash_password
from schemas import UserCreate, UserUpdate, UserResponse, MessageResponse
import crud
from logger import logger, log_action

# Khởi tạo DB tự động khi ứng dụng khởi động
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Đang khởi tạo cơ sở dữ liệu MySQL...")
    try:
        init_db()
        logger.info("Khởi tạo cơ sở dữ liệu thành công!")
    except Exception as e:
        logger.error(f"Khởi tạo CSDL thất bại: {e}")
    yield
    logger.info("Ứng dụng dừng hoạt động.")

app = FastAPI(
    title="Hệ thống Quản lý Người dùng (Lab 6)",
    description="Ứng dụng CRUD người dùng kết nối MySQL, FastAPI và giao diện Jinja2",
    version="1.0.0",
    lifespan=lifespan
)

# Cấu hình Templates Jinja2
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)
templates.env.filters["datetime_format"] = crud.format_datetime

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ============================================================================
# C. WEB UI ROUTES (Jinja2 + HTML Form)
# ============================================================================

@app.get("/", include_in_schema=False)
def root_redirect():
    """Điều hướng trang chủ về /users"""
    return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)

@app.get("/users", response_class=HTMLResponse, tags=["Web UI"])
def view_users_list(request: Request):
    """Route /users: hiển thị danh sách người dùng"""
    users = crud.get_all_users()
    return templates.TemplateResponse(
        request=request,
        name="users/index.html",
        context={"users": users}
    )

@app.get("/users/add", response_class=HTMLResponse, tags=["Web UI"])
def view_add_user_form(request: Request):
    """Route /users/add (GET): hiển thị form thêm người dùng"""
    return templates.TemplateResponse(
        request=request,
        name="users/add.html",
        context={}
    )

@app.post("/users/add", response_class=HTMLResponse, tags=["Web UI"])
def handle_add_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """Route /users/add (POST): xử lý thêm người dùng từ form"""
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return templates.TemplateResponse(
            request=request,
            name="users/add.html",
            context={
                "error": "Vui lòng điền đầy đủ tất cả các trường.",
                "name": name,
                "email": email
            },
            status_code=400
        )

    # Validate email trùng
    if crud.get_user_by_email(email):
        return templates.TemplateResponse(
            request=request,
            name="users/add.html",
            context={
                "error": f"Email '{email}' đã tồn tại trong hệ thống. Vui lòng chọn email khác.",
                "name": name,
                "email": email
            },
            status_code=400
        )

    # Mã hoá mật khẩu bằng bcrypt & lưu vào DB
    hashed = hash_password(password)
    new_user = crud.create_user(name, email, hashed)

    msg = quote(f"Thêm người dùng '{name}' thành công!")
    return RedirectResponse(url=f"/users?msg={msg}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/users/edit/{id}", response_class=HTMLResponse, tags=["Web UI"])
def view_edit_user_form(request: Request, id: int):
    """Route /users/edit/{id} (GET): form chỉnh sửa người dùng"""
    user = crud.get_user_by_id(id)
    if not user:
        err = quote("Người dùng không tồn tại.")
        return RedirectResponse(url=f"/users?error={err}", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request=request,
        name="users/edit.html",
        context={"user": user}
    )

@app.post("/users/edit/{id}", response_class=HTMLResponse, tags=["Web UI"])
def handle_edit_user(
    request: Request,
    id: int,
    name: str = Form(...),
    email: str = Form(...),
    password: Optional[str] = Form(None)
):
    """Route /users/edit/{id} (POST): xử lý cập nhật người dùng từ form"""
    user = crud.get_user_by_id(id)
    if not user:
        err = quote("Người dùng không tồn tại.")
        return RedirectResponse(url=f"/users?error={err}", status_code=status.HTTP_302_FOUND)

    name = name.strip()
    email = email.strip().lower()

    # Kiểm tra trùng email với người dùng khác
    existing_user = crud.get_user_by_email(email)
    if existing_user and existing_user["id"] != id:
        return templates.TemplateResponse(
            request=request,
            name="users/edit.html",
            context={
                "user": {"id": id, "name": name, "email": email, "created_at": user["created_at"]},
                "error": f"Email '{email}' đã được sử dụng bởi người dùng khác."
            },
            status_code=400
        )

    # Băm mật khẩu mới nếu có nhập
    hashed_pwd = hash_password(password.strip()) if password and password.strip() else None

    crud.update_user(id, name, email, hashed_pwd)
    msg = quote(f"Cập nhật thông tin #{id} thành công!")
    return RedirectResponse(url=f"/users?msg={msg}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/users/delete/{id}", response_class=HTMLResponse, tags=["Web UI"])
def view_delete_confirmation(request: Request, id: int):
    """Route /users/delete/{id} (GET): hiển thị trang xác nhận xoá"""
    user = crud.get_user_by_id(id)
    if not user:
        err = quote("Người dùng không tồn tại.")
        return RedirectResponse(url=f"/users?error={err}", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request=request,
        name="users/delete_confirm.html",
        context={"user": user}
    )

@app.post("/users/delete/{id}", tags=["Web UI"])
def handle_delete_user(id: int):
    """Route /users/delete/{id} (POST): thực hiện xoá người dùng"""
    user = crud.get_user_by_id(id)
    if not user:
        err = quote("Người dùng không tồn tại.")
        return RedirectResponse(url=f"/users?error={err}", status_code=status.HTTP_302_FOUND)

    crud.delete_user(id)
    msg = quote(f"Đã xoá người dùng '{user['name']}' thành công!")
    return RedirectResponse(url=f"/users?msg={msg}", status_code=status.HTTP_303_SEE_OTHER)


# ============================================================================
# B. REST API ENDPOINTS (FastAPI)
# ============================================================================

@app.get("/api/users", response_model=List[UserResponse], tags=["REST API"])
def api_get_users():
    """API GET /api/users: trả danh sách người dùng"""
    users = crud.get_all_users()
    return users

@app.get("/api/users/{id}", response_model=UserResponse, tags=["REST API"])
def api_get_user(id: int):
    """API GET /api/users/{id}: lấy thông tin 1 người"""
    user = crud.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng có ID={id}"
        )
    return user

@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["REST API"])
def api_create_user(payload: UserCreate):
    """
    API POST /api/users: tạo người dùng mới (JSON)
    - Validate email trùng -> trả lỗi 400
    - Mã hoá mật khẩu bằng bcrypt
    - Ghi log vào app.log
    """
    email = payload.email.strip().lower()
    if crud.get_user_by_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{email}' đã tồn tại trong hệ thống."
        )

    hashed = hash_password(payload.password)
    user = crud.create_user(payload.name.strip(), email, hashed)
    return user

@app.put("/api/users/{id}", response_model=UserResponse, tags=["REST API"])
def api_update_user(id: int, payload: UserUpdate):
    """
    API PUT /api/users/{id}: cập nhật thông tin người dùng
    - Validate email trùng nếu có thay đổi
    - Ghi log vào app.log
    """
    user = crud.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng có ID={id}"
        )

    name = payload.name.strip() if payload.name is not None else user["name"]
    email = payload.email.strip().lower() if payload.email is not None else user["email"]

    if payload.email is not None:
        existing = crud.get_user_by_email(email)
        if existing and existing["id"] != id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{email}' đã tồn tại cho người dùng khác."
            )

    hashed_pwd = hash_password(payload.password.strip()) if payload.password else None
    updated_user = crud.update_user(id, name, email, hashed_pwd)
    return updated_user

@app.delete("/api/users/{id}", response_model=MessageResponse, tags=["REST API"])
def api_delete_user(id: int):
    """
    API DELETE /api/users/{id}: xoá người dùng
    - Ghi log vào app.log
    """
    user = crud.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng có ID={id}"
        )

    crud.delete_user(id)
    return {"message": f"Đã xoá người dùng ID={id} ({user['name']}) thành công."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=APP_PORT, reload=True)
