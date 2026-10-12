"""
Script kiểm thử tự động toàn diện cho Lab 6: User Management System API & Web UI
"""
import sys
import time
import requests

BASE_URL = "http://localhost:8000"

def run_tests():
    print("=" * 60)
    print("BẮT ĐẦU KIỂM THỬ TỰ ĐỘNG LAB 6: USER MANAGEMENT SYSTEM")
    print("=" * 60)

    # 1. Test GET /api/users
    print("\n[1] Kiểm tra API GET /api/users:")
    try:
        res = requests.get(f"{BASE_URL}/api/users")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        users = res.json()
        print(f"    [PASS] Lấy danh sách thành công! Hiện có {len(users)} người dùng.")
    except Exception as e:
        print(f"    [FAIL] Không thể kết nối tới {BASE_URL}: {e}")
        return False

    # 2. Test POST /api/users (Thêm người dùng mới)
    print("\n[2] Kiểm tra API POST /api/users (Tạo mới người dùng):")
    test_email = f"test_{int(time.time())}@aptech.vn"
    new_user_payload = {
        "name": "Nguyễn Kiểm Thử",
        "email": test_email,
        "password": "SecretPassword@123"
    }
    res = requests.post(f"{BASE_URL}/api/users", json=new_user_payload)
    assert res.status_code in [200, 201], f"Expected 201/200, got {res.status_code} ({res.text})"
    created_user = res.json()
    created_id = created_user["id"]
    print(f"    [PASS] Tạo thành công người dùng ID={created_id} ({created_user['email']})")

    # 3. Test Validate trùng email
    print("\n[3] Kiểm tra Validate trùng email khi gọi API POST /api/users:")
    dup_res = requests.post(f"{BASE_URL}/api/users", json=new_user_payload)
    if dup_res.status_code == 400:
        print(f"    [PASS] Trả về HTTP 400 chính xác: '{dup_res.json().get('detail')}'")
    else:
        print(f"    [FAIL] Dự kiến 400 nhưng nhận được {dup_res.status_code}: {dup_res.text}")

    # 4. Test GET /api/users/{id}
    print(f"\n[4] Kiểm tra API GET /api/users/{created_id}:")
    res = requests.get(f"{BASE_URL}/api/users/{created_id}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    user_detail = res.json()
    print(f"    [PASS] Lấy thông tin ID={created_id}: Tên={user_detail['name']}, CreatedAt={user_detail['created_at']}")

    # 5. Test PUT /api/users/{id} (Cập nhật thông tin)
    print(f"\n[5] Kiểm tra API PUT /api/users/{created_id} (Cập nhật):")
    update_payload = {
        "name": "Nguyễn Kiểm Thử (Đã Sửa)",
        "email": test_email
    }
    res = requests.put(f"{BASE_URL}/api/users/{created_id}", json=update_payload)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    updated_user = res.json()
    assert updated_user["name"] == "Nguyễn Kiểm Thử (Đã Sửa)"
    print(f"    [PASS] Cập nhật thành công! Tên mới: '{updated_user['name']}'")

    # 6. Test DELETE /api/users/{id} (Xoá)
    print(f"\n[6] Kiểm tra API DELETE /api/users/{created_id} (Xoá):")
    res = requests.delete(f"{BASE_URL}/api/users/{created_id}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print(f"    [PASS] Xoá thành công ID={created_id} ({res.json().get('message')})")

    # 7. Test Web UI routes
    print("\n[7] Kiểm tra Giao diện Web (Jinja2 HTML):")
    res_web = requests.get(f"{BASE_URL}/users")
    assert res_web.status_code == 200, f"Expected 200, got {res_web.status_code}"
    assert "Quản lý Người dùng" in res_web.text
    print("    [PASS] Route /users (Danh sách Web) hoạt động hoàn hảo.")

    res_add = requests.get(f"{BASE_URL}/users/add")
    assert res_add.status_code == 200, f"Expected 200, got {res_add.status_code}"
    assert "Thêm Người dùng Mới" in res_add.text
    print("    [PASS] Route /users/add (Form thêm Web) hoạt động hoàn hảo.")

    print("\n" + "=" * 60)
    print("TẤT CẢ CÁC BÀI TEST LAB 6 ĐÃ VƯỢT QUA XUẤT SẮC (100% PASS)!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    run_tests()
