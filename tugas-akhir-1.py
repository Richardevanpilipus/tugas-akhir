import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Warna
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

# Membuat jendela game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Inisialisasi papan permainan
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Fungsi menggambar papan permainan
def draw_board():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Fungsi menggambar X atau O di kotak
def draw_symbols():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE), ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE), (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, LINE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2, LINE_WIDTH)

# Fungsi untuk mengecek kemenangan
def check_win(player):
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return True

    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True

    if all([board[i][i] == player for i in range(BOARD_COLS)]) or all([board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_COLS)]):
        return True

    return False

# Fungsi untuk mengecek apakah permainan seri
def check_draw():
    return all(all(cell != '' for cell in row) for row in board)

# Algoritma Minimax untuk pemain AI 'O'
def minimax(board, depth, maximizing_player):
    if check_win('O'):
        return 1
    elif check_win('X'):
        return -1
    elif check_draw():
        return 0

    if maximizing_player:
        max_eval = -float('inf')
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    max_eval = max(eval, max_eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    min_eval = min(eval, min_eval)
        return min_eval

# Fungsi untuk mengambil langkah terbaik AI 'O'
def ai_move():
    best_val = -float('inf')
    best_move = None

    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == '':
                board[i][j] = 'O'
                move_val = minimax(board, 0, False)
                board[i][j] = ''

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

# Variabel pemain yang sedang giliran
current_player = 'X'

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_player == 'X':
        # Pemain manusia
        if pygame.mouse.get_pressed()[0]:  # Mouse klik kiri
            x, y = pygame.mouse.get_pos()
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE

            if board[row][col] == '':
                board[row][col] = 'X'
                current_player = 'O'

    else:
        # Pemain AI
        move = ai_move()
        if move:
            row, col = move
            board[row][col] = 'O'
            current_player = 'X'

    screen.fill(WHITE)
    draw_board()
    draw_symbols()

    if check_win('X'):
        print("Player X Menang!")
        running = False
    elif check_win('O'):
        print("Player O Menang!")
        running = False
    elif check_draw():
        print("Permainan Seri!")
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()
