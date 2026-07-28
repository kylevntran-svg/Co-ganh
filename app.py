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

# --- LƯỚI ĐƯỜNG NỐI TỰ DO (KHÔNG CỐ ĐỊNH KÍCH THƯỚC) ---
# Dùng thuộc tính preserveAspectRatio="none" để nét vẽ tự động bám theo giao diện
svg_code = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
  <g stroke="#555555" stroke-width="1.2">
    <!-- Đường Ngang -->
    <line x1="10" y1="10" x2="90" y2="10"/>
    <line x1="10" y1="30" x2="90" y2="30"/>
    <line x1="10" y1="50" x2="90" y2="50"/>
    <line x1="10" y1="70" x2="90" y2="70"/>
    <line x1="10" y1="90" x2="90" y2="90"/>
    <!-- Đường Dọc -->
    <line x1="10" y1="10" x2="10" y2="90"/>
    <line x1="30" y1="10" x2="30" y2="90"/>
    <line x1="50" y1="10" x2="50" y2="90"/>
    <line x1="70" y1="10" x2="70" y2="90"/>
    <line x1="90" y1="10" x2="90" y2="90"/>
    <!-- Đường Chéo -->
    <line x1="10" y1="10" x2="90" y2="90"/>
    <line x1="90" y1="10" x2="10" y2="90"/>
    <line x1="50" y1="10" x2="10" y2="50"/>
    <line x1="50" y1="10" x2="90" y2="50"/>
    <line x1="10" y1="50" x2="50" y2="90"/>
    <line x1="90" y1="50" x2="50" y2="90"/>
  </g>
</svg>"""
b64_svg = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
bg_url = f"data:image/svg+xml;base64,{b64_svg}"

# --- CSS GIẢI PHÓNG HÌNH THỂ ---
st.markdown(f"""
    <style>
    h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {{
        color: #B4D4FF !important;
    }}
    
    /* 1. Trả tự do cho khung nền, xóa bỏ mọi thông số ép kích thước (width/height) */
    div[data-testid="stVerticalBlock"]:has(> div.element-container #board-anchor) {{
        background-image: url('{bg_url}') !important;
        background-size: 100% 100% !important; /* Tự động kéo dãn lưới vừa khít mọi cạnh */
        background-position: center !important;
        max-width: 450px !important; /* Chỉ khống chế không cho nó to bành trướng trên màn hình PC */
        margin: 20px auto !important;
        padding: 0 !important; /* Phải bằng 0 để đường nối chạm đúng tâm */
        background-color: transparent !important;
    }}

    /* 2. Ẩn điểm neo */
    div.element-container:has(#board-anchor) {{
        display: none !important;
    }}

    /* 3. Cho phép Streamlit tự chia khoảng cách giữa các hàng, chỉ cấm gap để toán học chuẩn xác */
    div[data-testid="stVerticalBlock"]:has(> div.element-container #board-anchor) > div[data-testid="stHorizontalBlock"] {{
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }}

    /* 4. Căn giữa quân cờ trong mỗi ô */
    div[data-testid="stVerticalBlock"]:has(> div.element-container #board-anchor) div[data-testid="column"] {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 10px 0 !important; /* Tạo độ thưa tự nhiên cho bàn cờ */
    }}

    /* 5. Nút cờ giữ nguyên form dáng */
    button[data-testid="baseButton-secondary"] {{
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        min-height: 44px !important;
        border-radius: 50% !important;
        background-color: #2e2e2e !important;
        border: 2px solid #444 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: transform 0.1s !important;
    }}
    button[data-testid="baseButton-secondary"]:hover {{
        border-color: #B4D4FF !important;
        transform: scale(1.1) !important;
    }}
    button[data-testid="baseButton-secondary"] p {{
        font-size: 20px !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- VẼ BÀN CỜ ---
with st.container():
    st.markdown('<div id="board-anchor"></div>', unsafe_allow_html=True)
    
    for r in range(5):
        # Dùng lại layout columns truyền thống của Streamlit, để nó tự lo việc co dãn
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