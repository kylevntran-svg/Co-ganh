import streamlit as st
import requests
import numpy as np
from co_ganh import CoGanh

# 🔴 ĐƯỜNG LINK FIREBASE CỦA BẠN (Đã được định dạng thẳng hàng)
FIREBASE_URL = "https://co-ganh-4fe17-default-rtdb.firebaseio.com/"

# --- CÁC HÀM GIAO TIẾP VỚI BỘ NÃO FIREBASE ---
def save_game_to_firebase(board, current_player, message):
    """Đẩy trạng thái bàn cờ lên đám mây (Không cần đẩy selected_piece để tối ưu tốc độ bấm)"""
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
    """Lấy trạng thái bàn cờ từ đám mây về"""
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
    save_game_to_firebase(game_logic.board, 1, "Trận đấu trực tuyến chính thức bắt đầu! Đỏ đi trước.")
    board_state = game_logic.board
    current_player = 1
    msg_state = "Trận đấu trực tuyến chính thức bắt đầu! Đỏ đi trước."
else:
    board_state = np.array(fb_data["board"])
    current_player = fb_data["current_player"]
    msg_state = fb_data["message"]

# Nạp dữ liệu vào lõi logic để tính toán nước đi hợp pháp
game_logic = CoGanh()
game_logic.board = board_state

# Khởi tạo bộ nhớ tạm chọn quân (Lưu local trong session_state để không bị reload trang)
if 'selected_piece' not in st.session_state:
    st.session_state.selected_piece = None

# --- GIAO DIỆN CHÍNH ---
st.title("Thưởng trà và cầm kì với Vịt 💖")

# Tạo 2 cột: cột trái hiện thông tin lượt đi, cột phải hiện hình ảnh bạn gái
col_turn, col_avatar = st.columns([2, 1])

with col_turn:
    if current_player == 1:
        st.subheader("🔴 Lượt của ĐỎ (Bạn)")
        st.write("Hãy tập trung đưa ra nước đi hiểm hóc nào! 🧠")
    else:
        st.subheader("🔵 Lượt của XANH (Bạn gái)")
        st.write("Đến lượt công chúa trổ tài gánh cờ rồi! ✨")

with col_avatar:
    try:
        if current_player == 1:
            st.image("gai_om_ga.jpg", width=120, caption="Đang chờ bạn gái...")
        else:
            st.image("gai_om_hoa.jpg", width=120, caption="Em yêu xinh hơn hoa")
    except:
        pass

st.info(msg_state)

# Nút bấm thủ công để tải nước đi mới của đối phương
if st.button("Cập nhật nước đi của đối phương 🔄", type="primary"):
    st.rerun()

st.write("---")

# --- TÙY CHỈNH CSS (Xanh pastel + Nút bấm tròn mượt mà) ---
st.markdown("""
    <style>
    /* Màu chữ xanh pastel ngọt ngào */
    h1, h2, h3, h4, h5, h6, p, span, caption, div[data-testid="stMarkdownContainer"] p {
        color: #B4D4FF !important;
    }
    /* Căn giữa nút bấm trong cột */
    div[data-testid="column"] { display: flex; justify-content: center; align-items: center; }
    /* Định dạng nút cờ hình tròn, mượt mà */
    button[data-testid="baseButton-secondary"] {
        font-size: 32px !important;
        height: 60px;
        width: 60px;
        border-radius: 50%;
        background-color: #2e2e2e;
        border: 2px solid #444;
        transition: all 0.1s ease-in-out;
    }
    button[data-testid="baseButton-secondary"]:hover {
        border-color: #B4D4FF;
        transform: scale(1.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- VẼ BÀN CỜ VÀ XỬ LÝ NƯỚC ĐI (Dùng nút bấm native, siêu mượt, không reload) ---
for r in range(5):
    cols = st.columns(5)
    for c in range(5):
        val = board_state[r, c]
        icon = "🔴" if val == 1 else "🔵" if val == -1 else "➕"
        
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
                        # Gọi logic di chuyển từ file co_ganh.py
                        success, next_msg = game_logic.move(sr, sc, r, c, current_player)
                        if success:
                            current_player *= -1  # Đổi lượt chơi
                        st.session_state.selected_piece = None
                        save_game_to_firebase(game_logic.board, current_player, next_msg)
                        st.rerun()

st.write("---")
if st.button("Làm mới toàn bộ bàn cờ (Reset) 🔄"):
    fresh_game = CoGanh()
    save_game_to_firebase(fresh_game.board, 1, "Ván mới đã được thiết lập từ đầu!")
    st.session_state.selected_piece = None
    st.rerun()