import streamlit as st
import requests
import numpy as np
import base64
from co_ganh import CoGanh
from streamlit_autorefresh import st_autorefresh

# 🔴 ĐƯỜNG LINK FIREBASE CỦA BẠN
FIREBASE_URL = "https://co-ganh-4fe17-default-rtdb.firebaseio.com/"

# --- BẬT CHẾ ĐỘ TỰ ĐỘNG LÀM MỚI ---
st_autorefresh(interval=2000, key="board_refresh")

# --- CÁC HÀM GIAO TIẾP VỚI BỘ NÃO FIREBASE ---
def save_game_to_firebase(board, current_player, message):
    data = {
        "board": board.tolist() if isinstance(board, np.ndarray) else board,
        "current_player": current_player,
        "message": message
    }
    try:
        requests.put(f"{FIREBASE_URL}game.json", json=data)
    except:
        pass

def load_game_from_firebase():
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
    save_game_to_firebase(game_logic.board, 1, "Đỏ đi trước.")
    board_state = game_logic.board
    current_player = 1
    msg_state = "Đỏ đi trước."
else:
    board_state = np.array(fb_data["board"])
    current_player = fb_data["current_player"]
    msg_state = fb_data["message"]

game_logic = CoGanh()
game_logic.board = board_state

if 'selected_piece' not in st.session_state:
    st.session_state.selected_piece = None

# --- GIAO DIỆN CHÍNH ---
st.title("Thưởng trà và cầm kì với Vịt 💖")

if current_player == 1:
    st.subheader("🔴 Lượt của ĐỎ")
else:
    st.subheader("🔵 Lượt của XANH")

st.info(msg_state)
st.write("---")

# --- MÃ HÓA HÌNH NỀN THEO TỌA ĐỘ MA TRẬN A1, B1 (Thang đo 0-100) ---
# Tọa độ các tâm chính xác là: 10, 30, 50, 70, 90
svg_code = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
  <g stroke="#666666" stroke-width="0.8">
    <!-- 3 Đường Ngang -->
    <line x1="10" y1="30" x2="90" y2="30"/>
    <line x1="10" y1="50" x2="90" y2="50"/>
    <line x1="10" y1="70" x2="90" y2="70"/>
    <!-- 3 Đường Dọc -->
    <line x1="30" y1="10" x2="30" y2="90"/>
    <line x1="50" y1="10" x2="50" y2="90"/>
    <line x1="70" y1="10" x2="70" y2="90"/>
    <!-- Chéo Chính (Đường X lớn) -->
    <line x1="10" y1="10" x2="90" y2="90"/>
    <line x1="90" y1="10" x2="10" y2="90"/>
    <!-- Chéo Phụ (Hình Thoi) -->
    <line x1="50" y1="10" x2="10" y2="50"/>
    <line x1="50" y1="10" x2="90" y2="50"/>
    <line x1="10" y1="50" x2="50" y2="90"/>
    <line x1="90" y1="50" x2="50" y2="90"/>
  </g>
</svg>"""
b64_svg = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
bg_url = f"data:image/svg+xml;base64,{b64_svg}"

# --- CSS: ÉP KHUNG TỰ ĐỘNG CO GIÃN THÀNH HÌNH VUÔNG ---
st.markdown(f"""
    <style>
    /* Chữ màu xanh pastel */
    h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {{
        color: #B4D4FF !important;
    }}
    
    /* Ẩn thẻ marker */
    div.element-container:has(.board-marker) {{
        display: none !important;
    }}

    /* 1. KHUNG BÀN CỜ: Luôn là hình vuông hoàn hảo (aspect-ratio: 1/1) */
    div[data-testid*="stVerticalBlock"]:has(> div.element-container .board-marker) {{
        width: 100% !important;
        max-width: 500px !important;
        aspect-ratio: 1 / 1 !important;
        margin: 20px auto !important;
        background-image: url('{bg_url}') !important;
        background-size: 100% 100% !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        padding: 0 !important;
        gap: 0 !important;
    }}

    /* 2. CÁC HÀNG: Chia đều 5 hàng, mỗi hàng chiếm đúng 20% chiều cao */
    div[data-testid*="stVerticalBlock"]:has(> div.element-container .board-marker) > div[data-testid*="stHorizontalBlock"] {{
        height: 20% !important;
        min-height: 20% !important;
        max-height: 20% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }}

    /* 3. CÁC CỘT: Chia đều 5 cột, mỗi cột chiếm đúng 20% chiều rộng */
    div[data-testid*="stVerticalBlock"]:has(> div.element-container .board-marker) div[data-testid*="column"] {{
        width: 20% !important;
        flex: 1 1 20% !important;
        height: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* 4. NÚT CỜ: Đặt cố định kích thước, luôn nằm chính giữa ô 20x20% */
    button[data-testid*="secondary"] {{
        width: 48px !important;
        height: 48px !important;
        border-radius: 50% !important;
        background-color: #1a1a1a !important; 
        border: 2px solid #555 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        z-index: 2 !important; 
        transition: transform 0.1s ease-in-out !important;
    }}
    button[data-testid*="secondary"]:hover {{
        border-color: #B4D4FF !important;
        transform: scale(1.15) !important;
    }}
    button[data-testid*="secondary"] p {{
        font-size: 24px !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- VẼ BÀN CỜ ---
with st.container():
    # Điểm đánh dấu (Marker) giúp CSS nhận diện chính xác vùng bàn cờ
    st.markdown('<div class="board-marker"></div>', unsafe_allow_html=True)

    # In 25 nút cờ, tự động được CSS ép vào đúng tọa độ lưới phần trăm
    for r in range(5):
        cols = st.columns(5)
        for c in range(5):
            val = board_state[r, c]
            icon = "🔴" if val == 1 else "🔵" if val == -1 else " "
            
            if st.session_state.selected_piece == (r, c):
                icon = "🔥"
                
            with cols[c]:
                if st.button(icon, key=f"btn_{r}_{c}"):
                    if st.session_state.selected_piece is None:
                        if val == current_player:
                            st.session_state.selected_piece = (r, c)
                            msg_state = "Đã chọn quân. Hãy click ô trống kề cạnh để đi."
                            save_game_to_firebase(board_state, current_player, msg_state)
                            st.rerun()
                    else:
                        sr, sc = st.session_state.selected_piece
                        if (r, c) == (sr, sc):
                            st.session_state.selected_piece = None
                            msg_state = "Đã hủy chọn quân."
                            save_game_to_firebase(board_state, current_player, msg_state)
                            st.rerun()
                        elif val == current_player:
                            st.session_state.selected_piece = (r, c)
                            msg_state = "Đã đổi sang quân cờ khác."
                            save_game_to_firebase(board_state, current_player, msg_state)
                            st.rerun()
                        elif val == 0:
                            success, next_msg = game_logic.move(sr, sc, r, c, current_player)
                            if success:
                                current_player *= -1
                            st.session_state.selected_piece = None
                            save_game_to_firebase(game_logic.board, current_player, next_msg)
                            st.rerun()

st.write("---")

if st.button("Làm mới toàn bộ bàn cờ (Reset) 🔄", type="primary"):
    fresh_game = CoGanh()
    save_game_to_firebase(fresh_game.board, 1, "Đỏ đi trước.")
    st.session_state.selected_piece = None
    st.rerun()