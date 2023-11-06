import math

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    scores = {
        'X': -1,
        'O': 1,
        'tie': 0
    }
    
    if check_winner(board, 'O'):
        return scores['O']
    if check_winner(board, 'X'):
        return scores['X']
    if is_full(board):
        return scores['tie']

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(eval, max_eval)
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(eval, min_eval)
        return min_eval

def best_move(board):
    best_eval = -math.inf
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = minimax(board, 0, False)
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)

    return best_move

def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print_board(board)

    while True:
        row, col = map(int, input("Enter row and column (0-2 separated by space): ").split())
        if board[row][col] == ' ':
            board[row][col] = 'X
        else:
            print("That cell is already occupied. Try again.")
            continue

        print_board(board)

        if check_winner(board, 'X'):
            print("You win!")
            break
        elif is_full(board):
            print("It's a tie!")
            break

        row, col = best_move(board)
        board[row][col] = 'O'
        print_board(board)

        if check_winner(board, 'O'):
            print("AI wins!")
            break
        elif is_full(board):
            print("It's a tie!")
            break

if __name__ == "__main__":
    main()
