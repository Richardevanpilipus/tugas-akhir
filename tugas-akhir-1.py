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
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 40
BUTTON_COLOR, BUTTON_HOVER_COLOR = (0, 128, 255), (0, 100, 200)  # Blue colors
WHITE, LINE_COLOR = (255, 255, 255), (0, 0, 0)


# Membuat jendela game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Inisialisasi papan permainan
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Variabel global game_over
game_over = False

# Variabel global first_move
first_move = True

def reset_game():
    global current_player, board, game_over, first_move
    first_move = not first_move
    if first_move:
        current_player = random.choice(["X", "O"])
    else:
        current_player = 'X'  # Atur pemain pertama secara manual
        
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False

    print(f"reset_game() called. current_player: {current_player}, first_move: {first_move}")

# Memanggil fungsi reset_game() untuk inisialisasi awal
reset_game()

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
                draw_x(row, col)
            elif board[row][col] == 'O':
                draw_o(row, col)

def draw_x(row, col):
    pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE), ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE), (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)

def draw_o(row, col):
    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.circle(screen, LINE_COLOR, center, SQUARE_SIZE // 2, LINE_WIDTH)

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
    
    if depth >= 1:
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


# Function to draw a button
def draw_button(rect, color, text, text_color):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, LINE_COLOR, rect, 2)

    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def is_mouse_over_button(rect):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return rect.collidepoint(mouse_x, mouse_y)

# Variabel pemain yang sedang giliran
current_player = random.choice(["X","O"])

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE

                if pygame.mouse.get_pressed()[0] and board[row][col] == '':
                    board[row][col] = 'X'
                    current_player = 'O'
                    print(f"Player X moves. current_player: {current_player}")

                    if check_win('X'):
                        print("Player X Menang!")
                        game_over = True
                    elif check_draw():
                        print("Permainan Seri!")
                        game_over = True
                    else:
                        move = ai_move()
                        if move:
                            ai_row, ai_col = move
                            board[ai_row][ai_col] = 'O'
                            current_player = 'X'
                            print(f"AI moves. current_player: {current_player}")

                            if check_win('O'):
                                print("Player O Menang!")
                                game_over = True
                            elif check_draw():
                                print("Permainan Seri!")
                                game_over = True
        # Logika restart
            restart_button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT - 60, BUTTON_WIDTH, BUTTON_HEIGHT)
            if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                reset_game()
                game_over = False  # Set game_over kembali ke False


    screen.fill(WHITE)
    draw_board()
    draw_symbols()

    if game_over:
        restart_button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT - 60, BUTTON_WIDTH, BUTTON_HEIGHT)
        restart_button_color = BUTTON_HOVER_COLOR if restart_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        draw_button(restart_button_rect, restart_button_color, "Restart", WHITE)
        
    pygame.display.update()
print(f"End of game loop. current_player: {current_player}")
pygame.quit()
sys.exit()
