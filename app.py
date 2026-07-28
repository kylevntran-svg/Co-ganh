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

# --- MÃ HÓA HÌNH NỀN THEO THANG ĐO 100x100 ---
svg_code = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
  <g stroke="#666666" stroke-width="0.8">
    <line x1="10" y1="30" x2="90" y2="30"/>
    <line x1="10" y1="50" x2="90" y2="50"/>
    <line x1="10" y1="70" x2="90" y2="70"/>
    <line x1="30" y1="10" x2="30" y2="90"/>
    <line x1="50" y1="10" x2="50" y2="90"/>
    <line x1="70" y1="10" x2="70" y2="90"/>
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

# --- TÍNH TOÁN MA TRẬN A1, B1... THEO CÔNG THỨC CỦA BẠN ---
css_positions = ""
for i in range(25):
    r = i // 5
    c = i % 5
    # Tọa độ tuyệt đối % (10, 30, 50, 70, 90)
    top = 10 + r * 20
    left = 10 + c * 20
    
    # nth-child bắt đầu từ 2 (vì số 1 là the div board-marker)
    css_positions += f"""
    div[data-testid="stVerticalBlock"]:has(.board-marker) > div.element-container:nth-child({i+2}) {{
        position: absolute !important;
        top: {top}% !important;
        left: {left}% !important;
        transform: translate(-50%, -50%) !important;
        width: 50px !important;
        height: 50px !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 10 !important;
    }}
    """

st.markdown(f"""
    <style>
    /* Chữ màu xanh pastel */
    h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {{
        color: #B4D4FF !important;
    }}
    
    /* 1. Ẩn điểm đánh dấu */
    div.element-container:has(.board-marker) {{
        display: none !important;
    }}

    /* 2. KHUNG BÀN CỜ CHÍNH: Ép thành hình vuông tĩnh 400x400 */
    div[data-testid="stVerticalBlock"]:has(.board-marker) {{
        position: relative !important;
        width: 400px !important;
        height: 400px !important;
        margin: 20px auto !important;
        background-image: url('{bg_url}') !important;
        background-size: 100% 100% !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
    }}

    /* 3. Bơm toàn bộ 25 tọa độ đã tính toán vào đây */
    {css_positions}

    /* 4. Định hình nút cờ (Chỉ áp dụng cho các nút bên trong bàn cờ) */
    div[data-testid="stVerticalBlock"]:has(.board-marker) button {{
        width: 50px !important;
        height: 50px !important;
        min-width: 50px !important;
        min-height: 50px !important;
        border-radius: 50% !important;
        background-color: #1a1a1a !important; 
        border: 2px solid #555 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: transform 0.1s ease-in-out !important;
    }}
    div[data-testid="stVerticalBlock"]:has(.board-marker) button:hover {{
        border-color: #B4D4FF !important;
        transform: scale(1.15) !important;
    }}
    div[data-testid="stVerticalBlock"]:has(.board-marker) button p {{
        font-size: 24px !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- VẼ BÀN CỜ (Không dùng st.columns nữa) ---
with st.container():
    # Điểm neo giúp CSS tìm đúng khung bàn cờ
    st.markdown('<div class="board-marker"></div>', unsafe_allow_html=True)

    # Đổ 25 quân cờ liên tục. CSS sẽ tự động bốc từng quân cờ ném vào đúng tọa độ A1, B1...
    for r in range(5):
        for c in range(5):
            val = board_state[r, c]
            icon = "🔴" if val == 1 else "🔵" if val == -1 else " "
            
            if st.session_state.selected_piece == (r, c):
                icon = "🔥"
                
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