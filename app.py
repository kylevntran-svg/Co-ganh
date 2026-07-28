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

# --- MÃ HÓA HÌNH NỀN SVG CHI TIẾT THEO ĐÚNG QUY LUẬT NỐI ĐƯỜNG CỦA BẠN ---
svg_code = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
  <g stroke="#666666" stroke-width="0.8">
    <!-- Hàng 1 (A1-E1) và kết nối -->
    <line x1="10" y1="10" x2="30" y2="10"/>
    <line x1="30" y1="10" x2="50" y2="10"/>
    <line x1="50" y1="10" x2="70" y2="10"/>
    <line x1="70" y1="10" x2="90" y2="10"/>
    
    <!-- Hàng 2 (A2-E2) và kết nối -->
    <line x1="10" y1="30" x2="30" y2="30"/>
    <line x1="30" y1="30" x2="50" y2="30"/>
    <line x1="50" y1="30" x2="70" y2="30"/>
    <line x1="70" y1="30" x2="90" y2="30"/>
    
    <!-- Hàng 3 (A3-E3) và kết nối -->
    <line x1="10" y1="50" x2="30" y2="50"/>
    <line x1="30" y1="50" x2="50" y2="50"/>
    <line x1="50" y1="50" x2="70" y2="50"/>
    <line x1="70" y1="50" x2="90" y2="50"/>
    
    <!-- Hàng 4 (A4-E4) và kết nối -->
    <line x1="10" y1="70" x2="30" y2="70"/>
    <line x1="30" y1="70" x2="50" y2="70"/>
    <line x1="50" y1="70" x2="70" y2="70"/>
    <line x1="70" y1="70" x2="90" y2="70"/>
    
    <!-- Hàng 5 (A5-E5) và kết nối -->
    <line x1="10" y1="90" x2="30" y2="90"/>
    <line x1="30" y1="90" x2="50" y2="90"/>
    <line x1="50" y1="90" x2="70" y2="90"/>
    <line x1="70" y1="90" x2="90" y2="90"/>

    <!-- Dọc 1 đến 5 (A-E) -->
    <line x1="10" y1="10" x2="10" y2="90"/>
    <line x1="30" y1="10" x2="30" y2="90"/>
    <line x1="50" y1="10" x2="50" y2="90"/>
    <line x1="70" y1="10" x2="70" y2="90"/>
    <line x1="90" y1="10" x2="90" y2="90"/>

    <!-- Các đường chéo theo chuẩn quy luật Cờ Gánh -->
    <line x1="10" y1="10" x2="90" y2="90"/>
    <line x1="90" y1="10" x2="10" y2="90"/>
    <line x1="50" y1="10" x2="10" y2="50"/>
    <line x1="50" y1="10" x2="90" y2="50"/>
    <line x1="10" y1="50" x2="50" y2="90"/>
    <line x1="90" y1="50" x2="50" y2="90"/>
    <line x1="50" y1="90" x2="10" y2="50"/>
    <line x1="50" y1="90" x2="90" y2="50"/>
    <line x1="10" y1="50" x2="50" y2="10"/>
    <line x1="90" y1="50" x2="50" y2="10"/>
  </g>
</svg>"""
b64_svg = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
bg_url = f"data:image/svg+xml;base64,{b64_svg}"

# --- CSS GRID CÁCH LY CHUẨN XÁC TUYỆT ĐỐI ---
st.markdown(f"""
    <style>
    /* Chữ màu xanh pastel */
    h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {{
        color: #B4D4FF !important;
    }}
    
    /* 1. KHUNG BÀN CỜ CHÍNH: Dùng CSS Grid ma trận 5x5 chuẩn chỉnh */
    .co-ganh-board {{
        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        grid-template-rows: repeat(5, 1fr) !important;
        width: 400px !important;
        height: 400px !important;
        margin: 20px auto !important;
        background-image: url('{bg_url}') !important;
        background-size: 100% 100% !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        padding: 0 !important;
        gap: 0 !important;
    }}

    /* 2. Căn chỉnh các phần tử container con bên trong lưới */
    .co-ganh-board > div.element-container {{
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* 3. Định hình nút bấm quân cờ hình tròn, bám chính xác vào giao điểm */
    .co-ganh-board button {{
        width: 45px !important;
        height: 45px !important;
        min-width: 45px !important;
        min-height: 45px !important;
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
    .co-ganh-board button:hover {{
        border-color: #B4D4FF !important;
        transform: scale(1.15) !important;
    }}
    .co-ganh-board button p {{
        font-size: 22px !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- VẼ BÀN CỜ ---
with st.container():
    # Mở khung chứa cách ly
    st.markdown('<div class="co-ganh-board">', unsafe_allow_html=True)
    
    # Vòng lặp rải 25 quân cờ trực tiếp vào lưới Grid 5x5
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
                        
    # Đóng khung chứa
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

if st.button("Làm mới toàn bộ bàn cờ (Reset) 🔄", type="primary"):
    fresh_game = CoGanh()
    save_game_to_firebase(fresh_game.board, 1, "Đỏ đi trước.")
    st.session_state.selected_piece = None
    st.rerun()