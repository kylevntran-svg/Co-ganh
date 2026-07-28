from flask import Flask, render_template, request, jsonify
import requests
import numpy as np
from co_ganh import CoGanh

app = Flask(__name__)

# 🔴 ĐƯỜNG LINK FIREBASE CỦA BẠN
FIREBASE_URL = "https://co-ganh-4fe17-default-rtdb.firebaseio.com/"

def get_db():
    try:
        res = requests.get(f"{FIREBASE_URL}game.json")
        if res.status_code == 200 and res.json():
            return res.json()
    except:
        pass
    
    # Khởi tạo mặc định nếu Firebase chưa có dữ liệu
    game = CoGanh()
    return {
        "board": game.board.tolist(),
        "current_player": 1,
        "message": "Đỏ đi trước.",
        "selected": None
    }

def save_db(data):
    try:
        requests.put(f"{FIREBASE_URL}game.json", json=data)
    except:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state', methods=['GET'])
def state():
    return jsonify(get_db())

@app.route('/click', methods=['POST'])
def click():
    data = request.json
    r, c = data['r'], data['c']
    
    db = get_db()
    board = np.array(db['board'])
    current_player = db['current_player']
    selected = db.get('selected')
    val = board[r, c]

    game = CoGanh()
    game.board = board

    if selected is None:
        if val == current_player:
            db['selected'] = [r, c]
            db['message'] = "Đã chọn quân. Hãy click ô trống kề cạnh để đi."
    else:
        sr, sc = selected
        if r == sr and c == sc:
            db['selected'] = None
            db['message'] = "Đã hủy chọn quân."
        elif val == current_player:
            db['selected'] = [r, c]
            db['message'] = "Đã đổi sang quân cờ khác."
        elif val == 0:
            success, next_msg = game.move(sr, sc, r, c, current_player)
            if success:
                db['current_player'] *= -1
                db['board'] = game.board.tolist()
            db['selected'] = None
            db['message'] = next_msg

    save_db(db)
    return jsonify(db)

@app.route('/reset', methods=['POST'])
def reset():
    game = CoGanh()
    db = {
        "board": game.board.tolist(),
        "current_player": 1,
        "message": "Đỏ đi trước.",
        "selected": None
    }
    save_db(db)
    return jsonify(db)

if __name__ == '__main__':
    # Chạy server Flask
    app.run(debug=True, port=5000)