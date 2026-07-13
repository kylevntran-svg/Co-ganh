import streamlit as st
import requests
import numpy as np
from co_ganh import CoGanh

# 🔴 THAY ĐƯỜNG LINK FIREBASE CỦA BẠN VÀO ĐÂY (Nhớ thẳng hàng, không xuống dòng giữa chừng nhé)
FIREBASE_URL = "https://co-ganh-4fe17-default-rtdb.firebaseio.com/"

# --- CÁC HÀM GIAO TIẾP VỚI BỘ NÃO FIREBASE ---
def save_game_to_firebase(board, current_player, message, selected_piece):
    """Đẩy toàn bộ trạng thái trận đấu và quân cờ đang chọn lên đám mây"""
    data = {
        "board": board.tolist() if isinstance(board, np.ndarray) else board,
        "current_player": current_player,
        "message": message,
        "selected_piece": selected_piece  # Lưu trạng thái chọn quân lên Firebase [r, c] hoặc None
    }
    try:
        requests.put(f"{FIREBASE_URL}game.json", json=data)
    except:
        pass

def load_game_from_firebase():
    """Lấy trạng thái trận đấu từ đám mây về"""
    try:
        res = requests.get(f"{FIREBASE_URL}game.json")
        if res.status_code == 200 and res.json():
            return res.json()
    except:
        return None
    return None

# --- KHỞI TẠO HOẶC ĐỒNG BỘ GAME TỪ CLOUD ---
fb_data = load_game_from_firebase()

if fb_data is None:
    game_logic = CoGanh()
    save_game_to_firebase(game_logic.board, 1, "Trận đấu trực tuyến bắt đầu! Đỏ đi trước.", None)
    board_state = game_logic.board
    current_player = 1
    msg_state = "Trận đấu trực tuyến bắt đầu! Đỏ đi trước."
    selected_piece = None
else:
    board_state = np.array(fb_data["board"])
    current_player = fb_data["current_player"]
    msg_state = fb_data["message"]
    # Ép kiểu dữ liệu mây về dạng tuple của Python
    selected_piece = fb_data.get("selected_piece", None)
    if selected_piece is not None:
        selected_piece = tuple(selected_piece)

# Nạp dữ liệu vào lõi logic để tính toán nước đi hợp pháp
game_logic = CoGanh()
game_logic.board = board_state

# --- XỬ LÝ SỰ KIỆN CLICK CHUỘT QUA URL (Khắc phục Amnesia bằng Firebase) ---
if "click" in st.query_params:
    click_pos = st.query_params["click"]
    st.query_params.clear()  # Xóa param để tránh lặp hành động
    
    r, c = map(int, click_pos.split("_"))
    val = board_state[r, c]
    
    if selected_piece is None:
        if val == current_player:
            selected_piece = (r, c)
            msg_state = "Đã chọn quân. Hãy click ô trống có đường nối kề cạnh để di chuyển!"
            save_game_to_firebase(board_state, current_player, msg_state, selected_piece)
        else:
            msg_state = "Ủa quân này đâu phải của bạn!"
            save_game_to_firebase(board_state, current_player, msg_state, selected_piece)
    else:
        sr, sc = selected_piece
        if (r, c) == (sr, sc):
            selected_piece = None
            msg_state = "Đã hủy chọn quân."
            save_game_to_firebase(board_state, current_player, msg_state, selected_piece)
        elif val == current_player:
            selected_piece = (r, c)
            msg_state = "Đã đổi sang quân cờ khác."
            save_game_to_firebase(board_state, current_player, msg_state, selected_piece)
        elif val == 0:
            # Chạy hàm kiểm tra và di chuyển từ file co_ganh.py gốc của bạn
            success, next_msg = game_logic.move(sr, sc, r, c, current_player)
            if success:
                current_player *= -1  # Đổi lượt
            selected_piece = None
            save_game_to_firebase(game_logic.board, current_player, next_msg, selected_piece)
        else:
            msg_state = "Không được đi đè lên quân đối phương nha!"
            save_game_to_firebase(board_state, current_player, msg_state, selected_piece)
    st.rerun()

# --- GIAO DIỆN CHÍNH ---
st.title("Thưởng trà và cầm kì với Vịt💖 - Cờ Gánh")

# Tạo 2 cột: cột trái hiện thông tin lượt đi, cột phải hiện hình ảnh bạn gái
col_turn, col_avatar = st.columns([2, 1])

with col_turn:
    if current_player == 1:
        st.subheader("🔴 Lượt của ĐỎ")
    else:
        st.subheader("🔵 Lượt của XANH")

with col_avatar:
    # Hiển thị hình ảnh tương ứng theo lượt đi cho sinh động
    try:
        if current_player == 1:
            # Khi tới lượt bạn (Đỏ), hiện hình ôm con gà tinh nghịch
            st.image("em_yeu_om_ga.jpg", width=120, caption="Đừng đi nước nào gà quá nha")
        else:
            # Khi tới lượt cô ấy (Xanh), hiện hình ôm bó hoa tươi tắn
            st.image("em_yeu_om_hoa.jpg", width=120, caption="Em yêu xinh hơn hoa")
    except:
        # Phòng trường hợp chưa load được ảnh thì bỏ qua không làm sập app
        pass

st.info(msg_state)

if st.button("Cập nhật nước đi của đối phương 🔄", type="primary"):
    st.rerun()

# --- DỰNG BÀN CỜ SVG CÓ ĐƯỜNG NỐI HỢP PHÁP ---
svg_bg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <line x1="40" y1="40" x2="360" y2="40" stroke="%23555555" stroke-width="2"/>
  <line x1="40" y1="120" x2="360" y2="120" stroke="%23555555" stroke-width="2"/>
  <line x1="40" y1="200" x2="360" y2="200" stroke="%23555555" stroke-width="2"/>
  <line x1="40" y1="280" x2="360" y2="280" stroke="%23555555" stroke-width="2"/>
  <line x1="40" y1="360" x2="360" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="40" y1="40" x2="40" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="120" y1="40" x2="120" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="200" y1="40" x2="200" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="280" y1="40" x2="280" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="360" y1="40" x2="360" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="40" y1="40" x2="360" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="360" y1="40" x2="40" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="200" y1="40" x2="40" y2="200" stroke="%23555555" stroke-width="2"/>
  <line x1="200" y1="40" x2="360" y2="200" stroke="%23555555" stroke-width="2"/>
  <line x1="40" y1="200" x2="200" y2="360" stroke="%23555555" stroke-width="2"/>
  <line x1="360" y1="200" x2="200" y2="360" stroke="%23555555" stroke-width="2"/>
</svg>
""".replace("\n", "").strip()

css_style = f"""
<style>
/* --- ĐỔI MÀU CHỮ SANG XANH PASTEL --- */
h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {{
    color: #B4D4FF !important;
}}

/* --- PHẦN CODE BÀN CỜ CŨ GIỮ NGUYÊN --- */
.board-container {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: repeat(5, 1fr);
    width: 100%;
    max-width: 420px;
    height: 420px;
    margin: 30px auto;
    background-image: url('data:image/svg+xml;utf8,{svg_bg}');
    background-size: 100% 100%;
    background-repeat: no-repeat;
    border: 3px solid #555;
    border-radius: 12px;
    padding: 8px;
    background-color: #1e1e1e;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.4);
}}
.cell-link {{
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    font-size: 34px;
    user-select: none;
    border-radius: 50%;
}}
.cell-link:hover {{
    background-color: rgba(255, 255, 255, 0.15);
    transform: scale(1.15);
    transition: all 0.1s ease-in-out;
}}
</style>
"""

board_html = '<div class="board-container">'
for r in range(5):
    for c in range(5):
        val = board_state[r, c]
        
        # Thiết lập icon chuẩn bài
        if val == 1:
            icon = "🔴"
        elif val == -1:
            icon = "🔵"
        else:
            icon = "➕"  # Trả về dấu cộng mảnh mai để lộ đường kẻ phía sau
            
        if selected_piece == (r, c):
            icon = "🔥"  # Hiệu ứng chọn quân bốc lửa
            
        board_html += f'<a class="cell-link" href="?click={r}_{c}" target="_self">{icon}</a>'

board_html += '</div>'
st.markdown(css_style + board_html, unsafe_allow_html=True)

st.write("---")
if st.button("Làm mới toàn bộ bàn cờ (Reset) 🔄"):
    fresh_game = CoGanh()
    save_game_to_firebase(fresh_game.board, 1, "Ván mới đã được thiết lập từ đầu!", None)
    st.rerun()