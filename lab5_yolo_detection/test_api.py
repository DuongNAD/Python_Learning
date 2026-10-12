"""
Script kiểm thử tự động cho Lab 5: YOLO Object Detection API
"""
import sys
import os
import requests

SERVER_URL = "http://localhost:8001"

def test_classes():
    print("1. Kiểm tra API GET /classes...")
    try:
        res = requests.get(f"{SERVER_URL}/classes")
        if res.status_code == 200:
            classes = res.json()
            print(f"   [PASS] Lấy danh sách thành công! Tổng số class: {len(classes)}")
            print(f"   Ví dụ một số class: {list(classes.values())[:10]}")
            return True
        else:
            print(f"   [FAIL] Status code: {res.status_code}, Body: {res.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Không thể kết nối tới {SERVER_URL}: {e}")
        return False

def test_upload(image_path: str):
    print(f"\n2. Kiểm tra API POST /upload với file '{image_path}'...")
    if not os.path.exists(image_path):
        print(f"   [WARN] Không tìm thấy file '{image_path}' để test upload.")
        return False

    try:
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
            res = requests.post(f"{SERVER_URL}/upload", files=files)

        if res.status_code == 200 and res.headers.get("content-type") == "image/jpeg":
            out_file = "result_test.jpg"
            with open(out_file, "wb") as out:
                out.write(res.content)
            print(f"   [PASS] Nhận diện thành công!")
            print(f"   - Header X-Detected-Objects-Count: {res.headers.get('x-detected-objects-count')}")
            print(f"   - Đã lưu ảnh kết quả có bounding boxes vào: '{out_file}'")
            return True
        else:
            print(f"   [FAIL] Status code: {res.status_code}, Response: {res.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Lỗi khi gửi request: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("BẮT ĐẦU KIỂM THỬ LAB 5 YOLO API")
    print("=" * 60)
    test_classes()
    sample_img = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    test_upload(sample_img)
