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

# --- MÃ HÓA CỨNG HÌNH NỀN BÀN CỜ (BASE64) ---
svg_code = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <line x1="40" y1="40" x2="360" y2="40" stroke="#555555" stroke-width="2"/>
  <line x1="40" y1="120" x2="360" y2="120" stroke="#555555" stroke-width="2"/>
  <line x1="40" y1="200" x2="360" y2="200" stroke="#555555" stroke-width="2"/>
  <line x1="40" y1="280" x2="360" y2="280" stroke="#555555" stroke-width="2"/>
  <line x1="40" y1="360" x2="360" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="40" y1="40" x2="40" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="120" y1="40" x2="120" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="200" y1="40" x2="200" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="280" y1="40" x2="280" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="360" y1="40" x2="360" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="40" y1="40" x2="360" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="360" y1="40" x2="40" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="200" y1="40" x2="40" y2="200" stroke="#555555" stroke-width="2"/>
  <line x1="200" y1="40" x2="360" y2="200" stroke="#555555" stroke-width="2"/>
  <line x1="40" y1="200" x2="200" y2="360" stroke="#555555" stroke-width="2"/>
  <line x1="360" y1="200" x2="200" y2="360" stroke="#555555" stroke-width="2"/>
</svg>"""
b64_svg = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
bg_url = f"data:image/svg+xml;base64,{b64_svg}"

# --- CSS THUẦN TÚY (Tương thích mọi trình duyệt web) ---
st.markdown(f"""
    <style>
    /* Chữ màu xanh pastel */
    h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {{
        color: #B4D4FF !important;
    }}
    
    /* 1. ÉP TẤT CẢ CÁC HÀNG (ROW) THÀNH CAO ĐÚNG 80px, RỘNG 400px */
    div[data-testid="stHorizontalBlock"] {{
        width: 400px !important;
        height: 80px !important;
        min-height: 80px !important;
        max-height: 80px !important;
        margin: 0 auto !important;
        padding: 0 !important;
        gap: 0 !important;
        position: relative !important;
        z-index: 10 !important;
    }}

    /* 2. ÉP TẤT CẢ CÁC CỘT TRONG HÀNG RỘNG ĐÚNG 80px */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
        width: 80px !important;
        min-width: 80px !important;
        max-width: 80px !important;
        height: 80px !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    /* 3. VẼ NỀN BÀN CỜ 400x400 TỪ HÀNG ĐẦU TIÊN PHỦ XUỐNG ĐÁY */
    div[data-testid="stHorizontalBlock"]:first-of-type::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 400px;
        height: 400px;
        background-image: url('{bg_url}');
        background-size: 100% 100%;
        border: 2px solid #555;
        border-radius: 12px;
        background-color: #1e1e1e;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.5);
        z-index: -1;
        pointer-events: none;
        box-sizing: border-box;
    }}

    /* 4. NẶN TẤT CẢ NÚT BẤM (CHỪA NÚT RESET) THÀNH HÌNH TRÒN 46x46px */
    button[data-testid="baseButton-secondary"] {{
        width: 46px !important;
        height: 46px !important;
        min-width: 46px !important;
        min-height: 46px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        margin: 0 auto !important;
        background-color: #2e2e2e !important;
        border: 2px solid #444 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.1s ease-in-out !important;
    }}
    button[data-testid="baseButton-secondary"]:hover {{
        border-color: #B4D4FF !important;
        transform: scale(1.1) !important;
    }}
    button[data-testid="baseButton-secondary"] p {{
        font-size: 20px !important;
        margin: 0 !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- VẼ BÀN CỜ ---
for r in range(5):
    # Tạo 5 cột sát rạt nhau
    cols = st.columns(5)
    for c in range(5):
        val = board_state[r, c]
        icon = "🔴" if val == 1 else "🔵" if val == -1 else " "
        
        if st.session_state.selected_piece == (r, c):
            icon = "🔥"
            
        with cols[c]:
            # Các nút cờ dùng style secondary, sẽ tự động bị ép tròn!
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

# Nút Reset dùng style primary nên CSS hình tròn sẽ tha cho nó
if st.button("Làm mới toàn bộ bàn cờ (Reset) 🔄", type="primary"):
    fresh_game = CoGanh()
    save_game_to_firebase(fresh_game.board, 1, "Đỏ đi trước.")
    st.session_state.selected_piece = None
    st.rerun()