import os
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List

import cv2
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import Response, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from ultralytics import YOLO

# Cấu hình đường dẫn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
LOG_FILE = os.path.join(BASE_DIR, "detection.log")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Cấu hình giới hạn
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Cấu hình Logging vào detection.log
detection_logger = logging.getLogger("yolo_detection")
detection_logger.setLevel(logging.INFO)
if not detection_logger.handlers:
    # Handler file
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    detection_logger.addHandler(fh)

    # Handler console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    detection_logger.addHandler(ch)

# Khởi tạo FastAPI
app = FastAPI(
    title="YOLO Object Detection API (Lab 5)",
    description="API nhận diện vật thể bằng YOLOv8 từ ảnh người dùng upload",
    version="1.0.0"
)

# Cấu hình Jinja2 templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Tải mô hình YOLOv8 nano (nhẹ, nhanh và chính xác cao)
print("Đang tải mô hình YOLOv8n...")
model = YOLO("yolov8n.pt")
print("Mô hình YOLOv8n sẵn sàng!")


@app.get("/", response_class=HTMLResponse, tags=["Web Test"])
def index(request: Request):
    """Giao diện Web trực quan để kiểm thử tải ảnh và nhận diện vật thể"""
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/classes", response_model=Dict[int, str], tags=["Detection API"])
def get_classes():
    """
    (Tùy chọn) API GET /classes:
    Trả về danh sách 80 classes của mô hình YOLOv8 (COCO dataset)
    """
    return model.names


@app.post("/upload", tags=["Detection API"])
async def upload_and_detect(file: UploadFile = File(...)):
    """
    API POST /upload nhận ảnh từ người dùng (form-data)
    - Kiểm tra định dạng hợp lệ: .jpg, .jpeg, .png
    - Hạn chế upload file > 5MB
    - Lưu ảnh tạm vào thư mục uploads/
    - Chạy nhận diện object trên ảnh vừa upload
    - Vẽ bounding boxes vào ảnh đầu ra
    - Trả ảnh đã nhận diện dạng image/jpeg trong response
    - Log các lần nhận diện thành công vào file detection.log
    """
    # 1. Kiểm tra định dạng file
    original_name = file.filename or "unknown"
    _, ext = os.path.splitext(original_name)
    ext = ext.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Định dạng file '{ext}' không hợp lệ. Chỉ chấp nhận các định dạng: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 2. Đọc nội dung file & kiểm tra dung lượng <= 5MB
    content = await file.read()
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File vượt quá dung lượng tối đa cho phép là 5MB (Kích thước hiện tại: {file_size / (1024*1024):.2f}MB)"
        )

    # 3. Lưu ảnh tạm vào thư mục uploads/
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    saved_path = os.path.join(UPLOADS_DIR, unique_filename)
    with open(saved_path, "wb") as f:
        f.write(content)

    try:
        # 4. Chạy mô hình YOLOv8 nhận diện object
        results = model(saved_path)
        first_result = results[0]

        # 5. Lấy danh sách các đối tượng nhận diện được để ghi log
        detected_objects = []
        if first_result.boxes is not None:
            for box in first_result.boxes:
                cls_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                cls_name = model.names.get(cls_id, f"class_{cls_id}")
                detected_objects.append(f"{cls_name} ({confidence*100:.1f}%)")

        # 6. Vẽ bounding boxes lên ảnh đầu ra
        annotated_frame = first_result.plot()

        # 7. Mã hoá ảnh đầu ra thành JPEG bytes
        success, encoded_image = cv2.imencode(".jpg", annotated_frame)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Không thể mã hoá ảnh kết quả sau khi nhận diện."
            )

        # 8. Log lần nhận diện thành công vào detection.log theo yêu cầu đề bài
        log_message = (
            f"Thành công | File: '{original_name}' (Lưu tạm: {unique_filename}) | "
            f"Dung lượng: {file_size / 1024:.1f} KB | "
            f"Số đối tượng: {len(detected_objects)} | "
            f"Chi tiết: [{', '.join(detected_objects) if detected_objects else 'Không phát hiện đối tượng nào'}]"
        )
        detection_logger.info(log_message)

        # 9. Trả ảnh đã nhận diện dạng image/jpeg trong response
        return Response(
            content=encoded_image.tobytes(),
            media_type="image/jpeg",
            headers={
                "X-Detected-Objects-Count": str(len(detected_objects)),
                "X-Original-Filename": original_name
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        detection_logger.error(f"Thất bại khi nhận diện ảnh '{original_name}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi trong quá trình xử lý ảnh: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
