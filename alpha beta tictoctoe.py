import os, math
import copy

# Định nghĩa các hằng số người chơi
X = "X"
O = "O"
# Bảng ban đầu chứa các số từ 1-9
INITIAL_BOARD_STATE = [*range(1, 10)]

# --- CÁC HÀM XỬ LÝ TRẠNG THÁI VÀ BÀN CỜ ---

def GetWinner(board):
    """
    Kiểm tra và trả về người chiến thắng ('X' hoặc 'O'), nếu không có trả về None.
    """
    winning_lines = [
        # horizontal
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        # vertical
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        # diagonal
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in winning_lines:
        # Điều kiện: 3 ô giống nhau VÀ ô đó phải là chuỗi (tức là 'X' hoặc 'O')
        if board[a] == board[b] and board[b] == board[c] and isinstance(board[a], str):
            return board[a]
            
    return None

def PrintBoard(board):
    """
    Xóa console và in bàn cờ hiện tại ra màn hình.
    """
    # Sử dụng cách hiển thị khác nếu đang chạy trong môi trường không hỗ trợ 'os.system' (ví dụ như Colab)
    # Tuy nhiên, giữ nguyên lệnh 'os.system' vì nó được yêu cầu trong mã gốc.
    if os.name == 'nt' or 'TERM' in os.environ:
        os.system('cls' if os.name=='nt' else 'clear')
        
    # Chuyển đổi các số thành khoảng trắng (hoặc giữ nguyên) để hiển thị rõ ràng hơn
    display_board = [str(c) if isinstance(c, int) else c for c in board]
    
    print(f'''
  {display_board[0]}|{display_board[1]}|{display_board[2]}
 --+-+-
  {display_board[3]}|{display_board[4]}|{display_board[5]}
 --+-+-
  {display_board[6]}|{display_board[7]}|{display_board[8]}
''')

def GetAvailableCells(board):
    """
    Trả về danh sách các ô còn trống (giá trị số từ 1-9).
    """
    available = []
    for cell in board:
        if isinstance(cell, int):
            available.append(cell)
    return available

# --- THUẬT TOÁN MINIMAX VỚI ALPHA-BETA ĐÃ TỐI ƯU HÓA COPY ---

def minimax(position, depth, alpha, beta, isMaximizing):
    """
    Hàm đệ quy Minimax với Alpha-Beta Pruning. 
    Sử dụng copy nông (shallow copy) để tránh thay đổi trạng thái gốc.
    """
    winner = GetWinner(position)
    
    # 1. Hàm đánh giá (Evaluation Function):
    if winner != None:
        if winner == X:
            return 10 - depth # Thắng nhanh (depth nhỏ) có giá trị cao hơn
        else: # winner == O
            return -10 + depth # Thua chậm (depth lớn) có giá trị cao hơn

    # Hòa
    if len(GetAvailableCells(position)) == 0:
        return 0

    if isMaximizing: # Lượt của X (tìm giá trị tối đa)
        maxEval = -math.inf
        
        for cell in GetAvailableCells(position):
            # Tạo bản sao độc lập cho mỗi nhánh đệ quy
            new_position = position[:] 
            
            new_position[cell - 1] = X
            Eval = minimax(new_position, depth + 1, alpha, beta, False)
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, Eval)
            
            if beta <= alpha:
                break 
        return maxEval
        
    else: # Lượt của O (tìm giá trị tối thiểu)
        minEval = +math.inf
        
        for cell in GetAvailableCells(position):
            # Tạo bản sao độc lập cho mỗi nhánh đệ quy
            new_position = position[:] 
            
            new_position[cell - 1] = O
            Eval = minimax(new_position, depth + 1, alpha, beta, True)
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            
            if beta <= alpha:
                break 
        return minEval

def FindBestMove(currentPosition, AI):
    """
    Tìm và trả về ô tối ưu nhất (index 1-9) cho AI.
    Sửa lỗi: Sử dụng bản sao để tránh làm hỏng bàn cờ gốc.
    """
    bestMove = -1
    
    if AI == X: # AI là Maximizer
        bestVal = -math.inf
        for cell in GetAvailableCells(currentPosition):
            # TẠO BẢN SAO ĐỂ THỬ NGHIỆM
            temp_position = currentPosition[:]
            temp_position[cell - 1] = AI
            
            # Lượt tiếp theo là của đối thủ (Minimizer = False)
            moveVal = minimax(temp_position, 0, -math.inf, +math.inf, False) 
            
            if moveVal > bestVal:
                bestMove = cell
                bestVal = moveVal
        return bestMove
        
    else: # AI là Minimizer
        bestVal = +math.inf
        for cell in GetAvailableCells(currentPosition):
            # TẠO BẢN SAO ĐỂ THỬ NGHIỆM
            temp_position = currentPosition[:]
            temp_position[cell - 1] = AI
            
            # Lượt tiếp theo là của đối thủ (Maximizer = True)
            moveVal = minimax(temp_position, 0, -math.inf, +math.inf, True)
            
            if moveVal < bestVal:
                bestMove = cell
                bestVal = moveVal
        return bestMove

# --- HÀM CHƠI CHÍNH ---

# --- HÀM CHƠI CHÍNH (ĐÃ SỬA LỖI KIỂM TRA) ---

# --- HÀM CHƠI CHÍNH ĐÃ SỬA LỖI HIỂN THỊ ---

def main():
    player = input("Bạn muốn chơi với ký hiệu X hay O? ").strip().upper()
    
    if player not in (X, O):
        print("Lựa chọn không hợp lệ. Mặc định bạn là X.")
        player = X
        
    AI = O if player == X else X
    currentGame = INITIAL_BOARD_STATE[:]
    currentTurn = X
    
    print(f"\nBạn là: {player} | AI là: {AI}")
    print("Các ô được đánh số từ 1 đến 9.")
    
    while True:
        
        # --- KIỂM TRA KẾT THÚC TRƯỚC (Dành cho lượt đi trước đó) ---
        winner_result = GetWinner(currentGame)
        if winner_result != None or not GetAvailableCells(currentGame):
            # *Đảm bảo in bàn cờ lần cuối trước khi thông báo kết quả*
            PrintBoard(currentGame)
            if winner_result == X:
                print("\n🏆 X là người chiến thắng!!!")
            elif winner_result == O:
                print("\n🏆 O là người chiến thắng!!!")
            else:
                print("\n🤝 Trò chơi Hòa.")
            break

        # 2. Lượt của AI
        if currentTurn == AI:
            print(f"\nĐến lượt AI ({AI}). Đang tính toán nước đi...")
            cell = FindBestMove(currentGame, AI)
            currentGame[cell - 1] = AI
            print(f"AI đi tới ô: {cell}")
            currentTurn = player
            
            # --- HIỂN THỊ VÀ KIỂM TRA NGAY SAU KHI AI ĐI ---
            # HIỂN THỊ bàn cờ sau nước đi của AI
            PrintBoard(currentGame) 
            
            # KIỂM TRA KẾT THÚC
            winner_result = GetWinner(currentGame)
            if winner_result != None or not GetAvailableCells(currentGame):
                if winner_result == X:
                    print("\n🏆 X là người chiến thắng!!!")
                elif winner_result == O:
                    print("\n🏆 O là người chiến thắng!!!")
                else:
                    print("\n🤝 Trò chơi Hòa.")
                break # KẾT THÚC VÒNG LẶP NẾU AI THẮNG HOẶC HÒA NGAY LẬP TỨC
            
        # 3. Lượt của Người chơi
        elif currentTurn == player:
            PrintBoard(currentGame) # Hiển thị bàn cờ trước khi người chơi đi
            while True:
                try:
                    humanInput = int(input("\nNhập số ô bạn muốn đi (1-9): ").strip())
                except ValueError:
                    PrintBoard(currentGame)
                    print("Lỗi: Đầu vào phải là số nguyên.")
                    continue
                    
                if humanInput in GetAvailableCells(currentGame):
                    currentGame[humanInput - 1] = player
                    currentTurn = AI
                    break
                else:
                    PrintBoard(currentGame)
                    print("Ô đã được đi hoặc không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
