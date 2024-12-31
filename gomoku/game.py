from typing import List, Tuple

class Gomoku:
    def __init__(self, size: int = 15) -> None:
        self.size: int = size
        self.board: List[List[str]] = [["." for _ in range(size)] for _ in range(size)]
        self.current_player: str = "X"  # X starts the game

    def display_board(self) -> None:
        # Print column numbers, adjust spacing to align with board content
        print("  " + " ".join(f"{i:2}" for i in range(self.size)))
        for i, row in enumerate(self.board):
            # Print row number and row content
            print(f"{i:2} " + " ".join(f"{cell:2}" for cell in row))
        print()

    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "."

    def place_stone(self, x: int, y: int) -> bool:
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            return True
        else:
            return False

    def check_win(self, x: int, y: int) -> bool:
        directions: List[Tuple[int, int]] = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count: int = 1
            for step in range(1, 5):
                nx, ny = x + dx * step, y + dy * step
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break

            for step in range(1, 5):
                nx, ny = x - dx * step, y - dy * step
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break

            if count >= 5:
                return True
        return False

    def switch_player(self) -> None:
        self.current_player = "O" if self.current_player == "X" else "X"

    def play(self) -> None:
        print("Welcome to Gomoku!")
        self.display_board()

        while True:
            try:
                print(f"Player {self.current_player}'s turn.")
                x, y = map(int, input("Enter your move (row, space, column): ").split())
                if self.place_stone(x, y):
                    self.display_board()
                    if self.check_win(x, y):
                        print(f"Player {self.current_player} wins!")
                        break
                    self.switch_player()
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter two integers separated by a space.")
            except KeyboardInterrupt:
                print("\nGame terminated.")
                break

if __name__ == "__main__":
    game = Gomoku()
    game.play()
