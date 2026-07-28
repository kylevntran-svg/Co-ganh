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

# --- MÃ HÓA HÌNH NỀN BÀN CỜ (Đúng chuẩn bản vẽ của bạn: Không có khung vuông ngoài) ---
svg_code = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <g stroke="#666666" stroke-width="3">
    <!-- 3 Đường Ngang Bên Trong -->
    <line x1="40" y1="120" x2="360" y2="120"/>
    <line x1="40" y1="200" x2="360" y2="200"/>
    <line x1="40" y1="280" x2="360" y2="280"/>
    <!-- 3 Đường Dọc Bên Trong -->
    <line x1="120" y1="40" x2="120" y2="360"/>
    <line x1="200" y1="40" x2="200" y2="360"/>
    <line x1="280" y1="40" x2="280" y2="360"/>
    <!-- Chéo Chính (Đường X lớn) -->
    <line x1="40" y1="40" x2="360" y2="360"/>
    <line x1="360" y1="40" x2="40" y2="360"/>
    <!-- Chéo Phụ (Hình Thoi) -->
    <line x1="200" y1="40" x2="40" y2="200"/>
    <line x1="200" y1="40" x2="360" y2="200"/>
    <line x1="40" y1="200" x2="200" y2="360"/>
    <line x1="360" y1="200" x2="200" y2="360"/>
  </g>
</svg>"""
b64_svg = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
bg_url = f"data:image/svg+xml;base64,{b64_svg}"

# --- CSS: ÉP QUÂN CỜ THÀNH HÌNH VUÔNG CHUẨN XÁC ---
st.markdown(f"""
    <style>
    h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {{
        color: #B4D4FF !important;
    }}
    
    /* 1. Ép toàn bộ khung bàn cờ thành Hình Vuông 400x400 và lót nền nét vẽ SVG */
    div[data-testid="stVerticalBlock"]:has(.board-wrapper):not(:has(div[data-testid="stVerticalBlock"]:has(.board-wrapper))) {{
        width: 400px !important;
        min-width: 400px !important;
        max-width: 400px !important;
        height: 400px !important;
        margin: 20px auto !important; /* Căn giữa màn hình */
        background-image: url('{bg_url}') !important;
        background-size: 400px 400px !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        padding: 0 !important;
        gap: 0 !important;
        background-color: transparent !important; /* Xóa nền xám, chỉ để lại nét kẻ */
    }}

    /* 2. Ẩn điểm neo để không chiếm chỗ */
    div.element-container:has(.board-wrapper) {{
        display: none !important;
    }}

    /* 3. Ép mỗi Hàng cờ cao đúng 80px */
    div[data-testid="stVerticalBlock"]:has(.board-wrapper) div[data-testid="stHorizontalBlock"] {{
        width: 400px !important;
        height: 80px !important;
        min-height: 80px !important;
        max-height: 80px !important;
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }}

    /* 4. CHÌA KHÓA CỦA BẠN ĐÂY: Vô hiệu hóa Flexbox, ép mỗi Cột cờ thành ô vuông 80x80px */
    div[data-testid="stVerticalBlock"]:has(.board-wrapper) div[data-testid="column"] {{
        width: 80px !important;
        min-width: 80px !important;
        max-width: 80px !important;
        height: 80px !important;
        flex: none !important; /* Lệnh "Cấm Streamlit tự động giãn ngang" */
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* 5. Nặn quân cờ thành hình tròn, bám chặt vào đường nối */
    button[data-testid="baseButton-secondary"] {{
        width: 46px !important;
        height: 46px !important;
        min-width: 46px !important;
        min-height: 46px !important;
        max-width: 46px !important;
        max-height: 46px !important;
        border-radius: 50% !important;
        background-color: #1e1e1e !important; 
        border: 2px solid #555 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: transform 0.15s ease-in-out !important;
    }}
    button[data-testid="baseButton-secondary"]:hover {{
        border-color: #B4D4FF !important;
        transform: scale(1.15) !important;
    }}
    button[data-testid="baseButton-secondary"] p {{
        font-size: 22px !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- VẼ BÀN CỜ ---
with st.container():
    # Điểm neo tàng hình giúp CSS nhắm đúng mục tiêu
    st.markdown('<div class="board-wrapper"></div>', unsafe_allow_html=True)
    
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