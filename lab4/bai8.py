"""
Bài 8 – Sử dụng pickle để lưu trạng thái đối tượng
Yêu cầu:
- Tạo class GameState với thuộc tính score, level.
- Lưu object GameState vào file state.dat bằng pickle.
- Đọc lại object từ file.
- In thông tin trạng thái.
- Xác minh object đọc lại giống với object gốc.
"""
import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "state.dat")

class GameState:
    """Class mô tả trạng thái game của người chơi"""
    def __init__(self, player_name: str, score: int, level: int):
        self.player_name = player_name
        self.score = score
        self.level = level

    def __eq__(self, other):
        """So sánh hai đối tượng GameState có cùng giá trị thuộc tính hay không"""
        if isinstance(other, GameState):
            return (self.player_name == other.player_name and
                    self.score == other.score and
                    self.level == other.level)
        return False

    def __str__(self):
        return f"GameState(Player='{self.player_name}', Score={self.score}, Level={self.level})"

def save_game_state(state: GameState, file_path: str = STATE_FILE):
    """Serialize đối tượng GameState vào file nhị phân bằng pickle"""
    with open(file_path, "wb") as f:
        pickle.dump(state, f)
    print(f"[+] Đã serialize đối tượng GameState vào file '{os.path.basename(file_path)}'")

def load_game_state(file_path: str = STATE_FILE) -> GameState:
    """Deserialize và phục hồi đối tượng GameState từ file nhị phân"""
    with open(file_path, "rb") as f:
        state = pickle.load(f)
    print(f"[+] Đã deserialize đối tượng GameState từ file '{os.path.basename(file_path)}'")
    return state

def main():
    print("=" * 60)
    print("BÀI 8: SỬ DỤNG PICKLE LƯU TRẠNG THÁI ĐỐI TƯỢNG (state.dat)")
    print("=" * 60)

    # 1. Khởi tạo đối tượng GameState ban đầu
    original_state = GameState(player_name="Antigravity_Hero", score=9850, level=15)
    print(f"\n[1] Đối tượng ban đầu (Original Object):")
    print(f"    {original_state}")
    print(f"    - Tên người chơi: {original_state.player_name}")
    print(f"    - Điểm số (score): {original_state.score}")
    print(f"    - Cấp độ (level):  {original_state.level}")

    # 2. Lưu object GameState vào file state.dat bằng pickle
    print(f"\n[2] Đang lưu trạng thái vào file...")
    save_game_state(original_state, STATE_FILE)

    # 3. Đọc lại object từ file
    print(f"\n[3] Đang nạp lại trạng thái từ file...")
    loaded_state = load_game_state(STATE_FILE)

    # 4. In thông tin trạng thái
    print(f"\n[4] Thông tin trạng thái sau khi đọc lại (Loaded Object):")
    print(f"    {loaded_state}")
    print(f"    - Tên người chơi: {loaded_state.player_name}")
    print(f"    - Điểm số (score): {loaded_state.score}")
    print(f"    - Cấp độ (level):  {loaded_state.level}")

    # 5. Xác minh object đọc lại giống với object gốc
    print("\n--- XÁC MINH TÍNH CHÍNH XÁC ---")
    print(f"ID bộ nhớ ban đầu: {id(original_state)}")
    print(f"ID bộ nhớ nạp lại: {id(loaded_state)}")
    is_identical = (original_state == loaded_state)
    print(f"Hai đối tượng có cùng giá trị dữ liệu? -> {is_identical}")

    if is_identical:
        print("\n[PASS] XÁC MINH THÀNH CÔNG: Đối tượng đọc lại hoàn toàn khớp 100% với đối tượng gốc!")
    else:
        print("\n[FAIL] Đối tượng không khớp!")

if __name__ == "__main__":
    main()
