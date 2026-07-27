import streamlit as st
import requests
import numpy as np
from co_ganh import CoGanh
from streamlit_autorefresh import st_autorefresh

# 🔴 ĐƯỜNG LINK FIREBASE CỦA BẠN
FIREBASE_URL = "https://co-ganh-4fe17-default-rtdb.firebaseio.com/"

# --- BẬT CHẾ ĐỘ TỰ ĐỘNG LÀM MỚI (AUTO-REFRESH) ---
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
    save_game_to_firebase(game_logic.board, 1, " Đỏ đi trước")
    board_state = game_logic.board
    current_player = 1
    msg_state = "Đỏ đi trước"
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

col_turn, col_avatar = st.columns([2, 1])

with col_turn:
    if current_player == 1:
        st.subheader("🔴 Lượt của ĐỎ")
    else:
        st.subheader("🔵 Lượt của XANH")
with col_avatar:
    try:
        if current_player == 1:
            st.image("em_yeu_om_ga.jpg", width=120)
        else:
            st.image("em_yeu_om_hoa.jpg", width=120)
    except:
        pass

st.info(msg_state)

st.write("---")

# --- MA THUẬT CSS MỚI: SỬA LỖI GIAO DIỆN TUYỆT ĐỐI ---
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

st.markdown(f"""
    <style>
    /* Chữ màu xanh pastel */
    h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {{
        color: #B4D4FF !important;
    }}
    
    /* 1. SỬA LỖI NỀN KHỔNG LỒ & CĂN KHUNG 400x400 TẬP TRUNG */
    div[data-testid="stVerticalBlock"]:has(.board-anchor):not(:has(div[data-testid="stVerticalBlock"]:has(.board-anchor))) {{
        background-image: url('data:image/svg+xml;utf8,{svg_bg}');
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
        width: 400px !important;
        max-width: 400px !important;
        height: 400px !important;
        margin: 20px auto !important;
        padding: 0 !important; /* Xóa khoảng trống thừa để căn giữa tuyệt đối */
        border: 3px solid #555 !important;
        border-radius: 12px !important;
        background-color: #1e1e1e !important;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.5) !important;
        overflow: hidden !important;
    }}
    
    /* 2. CHIA ĐỀU 5 HÀNG, MỖI HÀNG ĐÚNG 80px (80x5=400) */
    div[data-testid="stVerticalBlock"]:has(.board-anchor):not(:has(div[data-testid="stVerticalBlock"]:has(.board-anchor))) div[data-testid="stHorizontalBlock"] {{
        height: 80px !important;
        min-height: 80px !important;
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }}
    div[data-testid="stVerticalBlock"]:has(.board-anchor):not(:has(div[data-testid="stVerticalBlock"]:has(.board-anchor))) div[data-testid="column"] {{
        padding: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    /* 3. ÉP NÚT BẤM THÀNH HÌNH TRÒN HOÀN HẢO 50x50 */
    .stButton > button {{
        height: 50px !important;
        width: 50px !important;
        min-height: 50px !important;
        min-width: 50px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        background-color: #2e2e2e !important;
        border: 2px solid #444 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: auto !important;
        transition: all 0.1s ease-in-out !important;
    }}
    .stButton > button > div > p {{
        font-size: 24px !important;
        margin: 0 !important;
        line-height: 1 !important;
    }}
    .stButton > button:hover {{
        border-color: #B4D4FF !important;
        transform: scale(1.1) !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- VẼ BÀN CỜ ---
with st.container():
    # Nhúng mỏ neo ẩn để CSS nhắm trúng cái hộp này
    st.markdown('<span class="board-anchor" style="display:none;"></span>', unsafe_allow_html=True)
    
    for r in range(5):
        cols = st.columns(5)
        for c in range(5):
            val = board_state[r, c]
            # Dùng icon tàng hình cho ô trống để không đè lên đường kẻ
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
if st.button("Làm mới toàn bộ bàn cờ (Reset) 🔄"):
    fresh_game = CoGanh()
    save_game_to_firebase(fresh_game.board, 1, "Ván mới đã được thiết lập từ đầu!")
    st.session_state.selected_piece = None
    st.rerun()