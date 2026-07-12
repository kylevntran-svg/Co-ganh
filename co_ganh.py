import numpy as np

class CoGanh:
    def __init__(self):
        # 0: trống, 1: Bạn (Player 1), -1: Bạn gái (Player 2)
        self.board = np.array([
            [ 1,  1,  1,  1,  1],
            [ 1,  0,  0,  0,  1],
            [ 1,  0,  0,  0, -1],
            [-1,  0,  0,  0, -1],
            [-1, -1, -1, -1, -1]
        ])

    def get_adjacent(self, r, c):
        """Lấy danh sách các ô hợp lệ có thể đi tới từ ô (r, c)"""
        neighbors = []
        # Đi ngang, dọc
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 5 and 0 <= nc < 5:
                neighbors.append((nr, nc))
                
        # Đi chéo (chỉ áp dụng cho các ô có r + c chẵn)
        if (r + c) % 2 == 0:
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 5 and 0 <= nc < 5:
                    neighbors.append((nr, nc))
                    
        return neighbors

    def check_ganh(self, r, c, player):
        """Kiểm tra luật Gánh sau khi player vừa đi vào ô (r, c)"""
        # Danh sách các cặp hướng đối xứng (Dọc, Ngang)
        pairs = [ ((-1, 0), (1, 0)), ((0, -1), (0, 1)) ]
        
        # Nếu ô đích có đường chéo thì thêm hướng chéo vào để xét
        if (r + c) % 2 == 0:
            pairs.extend([ ((-1, -1), (1, 1)), ((-1, 1), (1, -1)) ])
        
        opponent = -player
        ganh_list = []
        
        for (dr1, dc1), (dr2, dc2) in pairs:
            r1, c1 = r + dr1, c + dc1
            r2, c2 = r + dr2, c + dc2
            
            if (0 <= r1 < 5 and 0 <= c1 < 5) and (0 <= r2 < 5 and 0 <= c2 < 5):
                # Nếu cả 2 ô đối xứng đều là quân địch -> Gánh!
                if self.board[r1, c1] == opponent and self.board[r2, c2] == opponent:
                    ganh_list.extend([(r1, c1), (r2, c2)])
        
        # Đổi màu quân bị gánh thành quân của mình
        for (gr, gc) in ganh_list:
            self.board[gr, gc] = player

    def check_vay(self, target_player):
        """Kiểm tra và bắt các quân địch bị Vây (không còn đường đi)"""
        visited = set()
        captured_pieces = []
        
        for r in range(5):
            for c in range(5):
                if self.board[r, c] == target_player and (r, c) not in visited:
                    # Dùng BFS để kiểm tra toàn bộ cụm quân
                    group = []
                    queue = [(r, c)]
                    visited.add((r, c))
                    has_liberty = False # Biến kiểm tra xem cụm này còn "đường sống" không
                    
                    while queue:
                        curr_r, curr_c = queue.pop(0)
                        group.append((curr_r, curr_c))
                        
                        for nr, nc in self.get_adjacent(curr_r, curr_c):
                            if self.board[nr, nc] == 0:
                                has_liberty = True # Phát hiện còn ô trống bên cạnh -> Sống!
                            elif self.board[nr, nc] == target_player and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))
                    
                    # Nếu check xong cả cụm mà không có "đường sống", đưa vào danh sách tử hình
                    if not has_liberty:
                        captured_pieces.extend(group)
                        
        # Đổi màu quân bị vây
        for (cr, cc) in captured_pieces:
            self.board[cr, cc] = -target_player # -target_player chính là mình

    def move(self, r1, c1, r2, c2, current_player):
        """Thực hiện một nước đi hoàn chỉnh"""
        if self.board[r1, c1] != current_player:
            return False, "Đây không phải quân của bạn!"
            
        if self.board[r2, c2] != 0:
            return False, "Ô đích đã có quân!"
            
        if (r2, c2) not in self.get_adjacent(r1, c1):
            return False, "Nước đi sai luật (không có đường nối hoặc đi quá xa)!"
            
        # 1. Di chuyển quân
        self.board[r2, c2] = current_player
        self.board[r1, c1] = 0
        
        # 2. Xử lý Gánh (Bắt quân địch bị kẹp)
        self.check_ganh(r2, c2, current_player)
        
        # 3. Xử lý Vây (Bắt các cụm quân địch bị hết đường đi)
        self.check_vay(-current_player)
        
        return True, "Nước đi hợp lệ!"

    def check_win(self):
        """Kiểm tra xem có ai thắng chưa"""
        if np.all(self.board != -1):
            return 1 # Player 1 thắng
        if np.all(self.board != 1):
            return -1 # Player 2 thắng
        return 0 # Chưa ai thắng

    def display(self):
        print("Bàn cờ hiện tại:")
        print(self.board)
        print("-" * 20)

# --- CHẠY THỬ LOGIC ---
if __name__ == "__main__":
    game = CoGanh()
    game.display()
    
    # Giả sử Player 1 (số 1) đi một nước thử nghiệm: từ (2,0) sang (2,1)
    # (Bạn có thể đổi tọa độ để test các trường hợp Gánh/Vây)
    success, message = game.move(2, 0, 2, 1, 1)
    print(message)
    game.display()