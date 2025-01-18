from enum import Enum
from typing import List, Optional, Tuple

from gomoku.visualizer import Visualizer

class Status(Enum):
    OPEN = 1
    WIN_X = 2
    WIN_O = 3
    INVALID = 4

class Gomoku:
    def __init__(self, size: int = 15, visualizer: Optional[Visualizer] = None) -> None:
        self.size = size
        self.board: List[List[str]] = [["." for _ in range(size)] for _ in range(size)]
        self.current_player: str = "X"  # X starts the game
        self.visualizer = visualizer

    def make_move(self, x: int, y: int) -> Status:
        if self.place_stone(x, y):
            if self.check_win(x, y):
                return Status.WIN_X if self.current_player == "X" else Status.WIN_O
            self.switch_player()
            return Status.OPEN
        else:
            print("Invalid move. Try again.")
            return Status.INVALID

    def play(self) -> None:
        print("Welcome to Gomoku!")
        status = Status.OPEN

        while True:
            try:
                self.visualizer.display_board(self.board)
                position = self.visualizer.get_next_position()

                x, y = position
                status = self.make_move(x, y)

                if status == Status.WIN_X or status == Status.WIN_O:
                    winner = "X" if status == Status.WIN_X else "O"
                    self.visualizer.display_board(self.board, winner=winner)
                    print(f"Player {winner} wins!")
                    break

            except KeyboardInterrupt:
                print("\nGame terminated.")
                break

    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "."

    def place_stone(self, x: int, y: int) -> bool:
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            return True
        return False

    def check_win(self, x: int, y: int) -> bool:
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for step in range(1, 5):
                nx, ny = x + step * dx, y + step * dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break
            for step in range(1, 5):
                nx, ny = x - step * dx, y - step * dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def switch_player(self) -> None:
        self.current_player = "O" if self.current_player == "X" else "X"