class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def print_board(self):
        for i in range(0, 9, 3):
            print(" | ".join(self.board[i:i+3]))
            if i < 6:
                print("-" * 9)

    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
        else:
            print("Invalid move. Try again.")

    def check_win(self):
        win_patterns = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != " ":
                return True
        return False

    def check_draw(self):
        return " " not in self.board

    def play_game(self):
        while True:
            self.print_board()
            move = int(input(f"Player {self.current_player}, enter your move (0-8): "))
            if 0 <= move <= 8:
                self.make_move(move)
                if self.check_win():
                    self.print_board()
                    print(f"Player {self.current_player} wins!")
                    break
                if self.check_draw():
                    self.print_board()
                    print("It's a draw!")
                    break
            else:
                print("Invalid input. Enter a number between 0 and 8.")

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
