import copy
import math
import random
import numpy

# Định nghĩa các hằng số
X = "X"
O = "O"
EMPTY = None
user = None
ai = None
    
def initial_state():
    """
    Trả về trạng thái ban đầu của bàn cờ.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Trả về người chơi có lượt đi tiếp theo trên bàn cờ.
    """
    count = 0
    for row in board:
        for cell in row:
            if cell is not EMPTY:
                count += 1
    
    # Nếu số nước đi là chẵn (0, 2, 4, 6, 8), X đi.
    # Nếu số nước đi là lẻ (1, 3, 5, 7), O đi.
    # Logic này phải phù hợp với cách bạn gán user/ai.
    if count % 2 == 0:
        return X  # X luôn đi trước
    else:
        return O

def actions(board):
    """
    Trả về tập hợp tất cả các hành động có thể (i, j) trên bàn cờ.
    """
    res = set()
    board_len = len(board)
    for i in range(board_len):
        for j in range(board_len):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res

def result(board, action):
    """
    Trả về bàn cờ mới sau khi thực hiện nước đi (i, j).
    """
    # Không cần kiểm tra tính hợp lệ ở đây vì hàm minimax chỉ gọi actions() hợp lệ
    curr_player = player(board)
    # Sao chép sâu để tránh sửa đổi trạng thái gốc
    result_board = copy.deepcopy(board)
    (i, j) = action
    result_board[i][j] = curr_player
    return result_board

def get_horizontal_winner(board):
    """Kiểm tra người thắng theo hàng ngang."""
    board_len = len(board)
    for i in range(board_len):
        if board[i][0] is not EMPTY and all(board[i][j] == board[i][0] for j in range(board_len)):
            return board[i][0]
    return None

def get_vertical_winner(board):
    """Kiểm tra người thắng theo hàng dọc."""
    board_len = len(board)
    for j in range(board_len):
        if board[0][j] is not EMPTY and all(board[i][j] == board[0][j] for i in range(board_len)):
            return board[0][j]
    return None

def get_diagonal_winner(board):
    """Kiểm tra người thắng theo đường chéo."""
    board_len = len(board)
    
    # Đường chéo chính (0,0), (1,1), (2,2)
    if board[0][0] is not EMPTY and all(board[i][i] == board[0][0] for i in range(board_len)):
        return board[0][0]
        
    # Đường chéo phụ (0,2), (1,1), (2,0)
    if board[0][board_len - 1] is not EMPTY and all(board[i][board_len - 1 - i] == board[0][board_len - 1] for i in range(board_len)):
        return board[0][board_len - 1]
        
    return None

def winner(board):
    """
    Trả về người thắng của trò chơi, nếu có.
    """
    # SỬA LỖI CÚ PHÁP: Sử dụng 'or' giữa các hàm một cách rõ ràng
    winner_val = get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_winner(board)
    return winner_val

def terminal(board):
    """
    Trả về True nếu trò chơi kết thúc, False nếu chưa.
    """
    if winner(board) is not None:
        return True
    
    # Kiểm tra còn ô trống hay không (Hòa)
    return not actions(board)

def utility(board):
    """
    Trả về 1 nếu X thắng, -1 nếu O thắng, 0 nếu hòa.
    """
    winner_val = winner(board)
    if winner_val == X:
        return 1
    elif winner_val == O:
        return -1
    return 0

# ----------------- Thuật toán Minimax -----------------

def maxValue(state):
    """Trả về giá trị tối đa có thể đạt được từ trạng thái này."""
    if terminal(state):
        return utility(state)
    
    v = -math.inf
    for action in actions(state):
        v = max(v, minValue(result(state, action)))
    return v

def minValue(state):
    """Trả về giá trị tối thiểu có thể đạt được từ trạng thái này."""
    if terminal(state):
        return utility(state)
        
    v = math.inf
    for action in actions(state):
        v = min(v, maxValue(result(state, action)))
    return v

def minimax(board):
    """
    Trả về hành động tối ưu cho người chơi hiện tại trên bàn cờ.
    SỬA LỖI LOGIC: Đảm bảo người chơi Max tìm Max và người chơi Min tìm Min.
    """
    current_player = player(board)

    if current_player == X:  # X là người chơi Max (tìm giá trị 1)
        max_value = -math.inf
        optimal_move = None
        
        for action in actions(board):
            # X muốn Maximize, nên gọi MinValue cho trạng thái tiếp theo
            check_value = minValue(result(board, action)) 
            if check_value > max_value: 
                max_value = check_value
                optimal_move = action
        return optimal_move

    else:  # O là người chơi Min (tìm giá trị -1)
        min_value = math.inf
        optimal_move = None
        
        for action in actions(board):
            # O muốn Minimize, nên gọi MaxValue cho trạng thái tiếp theo
            check_value = maxValue(result(board, action)) 
            if check_value < min_value:
                min_value = check_value
                optimal_move = action
        return optimal_move

# ----------------- Vòng lặp Trò chơi -----------------

if __name__ == "__main__":
    board = initial_state()
    
    # Thiết lập người chơi
    print("Chọn người chơi (X hoặc O):")
    chosen_player = input().upper()
    if chosen_player == "X":
        user = X
        ai = O
    elif chosen_player == "O":
        user = O
        ai = X
    else:
        print("Lựa chọn không hợp lệ. Mặc định bạn là X, AI là O.")
        user = X
        ai = O

    print(f"\nBạn là: {user}, AI là: {ai}")
    print("Bắt đầu trò chơi:\n")
    print(numpy.array(board))

    # SỬA LỖI LOGIC: Vòng lặp chơi game
    while True:
        current_player = player(board)

        if terminal(board):
            win_result = winner(board)
            if win_result is None:
                print("\nKết thúc: HÒA.")
            else:
                print(f"\nKết thúc: {win_result} THẮNG!")
            break
        
        # Lượt của Người dùng
        if current_player == user:
            print("\nĐến lượt bạn. Nhập vị trí (hàng,cột) [0-2, 0-2]")
            try:
                i = int(input("Hàng:"))
                j = int(input("Cột:"))
                move = (i, j)
            except ValueError:
                print("Lỗi: Đầu vào phải là số nguyên.")
                continue

            if 0 <= i <= 2 and 0 <= j <= 2 and board[i][j] == EMPTY:
                board = result(board, move)
                print(numpy.array(board))
            else:
                print("Nước đi không hợp lệ. Vui lòng thử lại.")
        
        # Lượt của AI
        elif current_player == ai:
            print(f"\nĐến lượt AI ({ai}). Đang tính toán nước đi...")
            
            # Sử dụng thuật toán Minimax để tìm nước đi tối ưu
            move = minimax(board)
            
            board = result(board, move)
            print(f"AI đi tới: {move}")
            print(numpy.array(board))
