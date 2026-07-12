import streamlit as st
from co_ganh import CoGanh

# --- 1. KHỞI TẠO STATE TRẬN ĐẤU ---
if 'game' not in st.session_state:
    st.session_state.game = CoGanh()
if 'selected_piece' not in st.session_state:
    st.session_state.selected_piece = None
if 'current_player' not in st.session_state:
    st.session_state.current_player = 1
if 'message' not in st.session_state:
    st.session_state.message = "Game On! Bắt đầu ván cờ gánh nào!"

# --- GIAO DIỆN CHÍNH ---
st.title("Thưởng trà cầm kì thi họa cũng Vịt yêu 💖")
player_name = "🔴 Lượt của Đỏ" if st.session_state.current_player == 1 else "🔵 Lượt của Xanh"
st.subheader(player_name)

if st.session_state.message:
    st.info(st.session_state.message)

# --- TÙY CHỈNH CSS ĐỂ CĂN CHỈNH NÚT BẤM ---
st.markdown("""
    <style>
    /* Ép các cột canh giữa và thu gọn khoảng cách */
    div[data-testid="column"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* Phóng to icon trong nút bấm để nhìn giống quân cờ */
    button[data-testid="baseButton-secondary"] {
        font-size: 32px !important;
        height: 60px;
        width: 60px;
        border-radius: 50%;
        background-color: #2e2e2e;
        border: 2px solid #444;
    }
    button[data-testid="baseButton-secondary"]:hover {
        border-color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.write("---")

# --- 2. VẼ BÀN CỜ (DÙNG ST.BUTTON ĐỂ KHÔNG MẤT TRÍ NHỚ GAME) ---
board = st.session_state.game.board

for r in range(5):
    cols = st.columns(5)
    for c in range(5):
        val = board[r, c]
        
        # Gán icon cho các giá trị
        if val == 1:
            icon = "🔴"
        elif val == -1:
            icon = "🔵"
        else:
            icon = "➕" # TRẢ LẠI DẤU CỘNG CHUẨN BÀI!
            
        # Đổi thành lửa nếu đang được chọn
        if st.session_state.selected_piece == (r, c):
            icon = "🔥"
            
        with cols[c]:
            if st.button(icon, key=f"btn_{r}_{c}"):
                # Logic xử lý click chuột chuẩn xác
                if st.session_state.selected_piece is None:
                    if val == st.session_state.current_player:
                        st.session_state.selected_piece = (r, c)
                        st.session_state.message = "Đã chọn quân. Hãy click ô trống kề cạnh để đi."
                    else:
                        st.session_state.message = "Hãy chọn lại"
                else:
                    sr, sc = st.session_state.selected_piece
                    if (r, c) == (sr, sc):
                        st.session_state.selected_piece = None
                        st.session_state.message = "Đã hủy chọn quân."
                    elif val == st.session_state.current_player:
                        st.session_state.selected_piece = (r, c)
                        st.session_state.message = "Đã đổi sang quân cờ khác."
                    elif val == 0:
                        success, msg = st.session_state.game.move(sr, sc, r, c, st.session_state.current_player)
                        st.session_state.message = msg
                        if success:
                            st.session_state.current_player *= -1
                        st.session_state.selected_piece = None
                    else:
                        st.session_state.message = "Không đi đè lên quân đối phương"
                
                st.rerun()

st.write("---")
if st.button("Reset Game 🔄", type="primary"):
    st.session_state.game = CoGanh()
    st.session_state.selected_piece = None
    st.session_state.current_player = 1
    st.session_state.message = "Trận mới sẵn sàng"
    st.rerun()