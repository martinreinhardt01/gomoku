from typing import List, Optional, Tuple

from gomoku.visualizer import GomokuVisualizer
# Import the visualizer only if you want type hints
# (use TYPE_CHECKING if you want to avoid import cycles).
# from gomoku.visualizer import GomokuVisualizer

class Gomoku:
    def __init__(self, size: int = 15, visualizer:Optional[GomokuVisualizer] = None) -> None:
        """
        The core Gomoku game logic (no direct rendering code).
        If a visualizer is provided, it should have a `render_board` method
        that takes board and winner as arguments and returns an (x, y) click
        or None.
        """
        self.size = size
        self.board: List[List[str]] = [["." for _ in range(size)] for _ in range(size)]
        self.current_player: str = "X"  # X starts the game
        # The visualizer is injected from outside. Make it Optional.
        self.visualizer = visualizer

    def display_board(self, winner: Optional[str] = None) -> Optional[Tuple[int, int]]:
        """
        Requests the visualizer to show the board and returns the position
        the user clicked, if a visualizer is provided. Otherwise, prints
        the board to the console.
        """
        if self.visualizer:
            return self.visualizer.render_board(self.board, winner)
        else:
            # Fallback: print to console
            for row in self.board:
                print(" ".join(row))
            if winner:
                print(f"Player {winner} wins!")
            return None

    def is_valid_move(self, x: int, y: int) -> bool:
        """
        Checks if the move (x, y) is within the board and the cell is not occupied.
        """
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "."

    def place_stone(self, x: int, y: int) -> bool:
        """
        Place a stone on the board if valid. Returns True if successful, False otherwise.
        """
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            return True
        return False

    def check_win(self, x: int, y: int) -> bool:
        """
        Checks if the current_player has won after placing a stone at (x, y).
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            # Move in the positive direction (up to 4 steps)
            for step in range(1, 5):
                nx, ny = x + dx * step, y + dy * step
                if 0 <= nx < self.size and 0 <= ny < self.size \
                   and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break

            # Move in the negative direction (up to 4 steps)
            for step in range(1, 5):
                nx, ny = x - dx * step, y - dy * step
                if 0 <= nx < self.size and 0 <= ny < self.size \
                   and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break

            if count >= 5:
                return True
        return False

    def switch_player(self) -> None:
        """
        Switches the current player from X to O, or O to X.
        """
        self.current_player = "O" if self.current_player == "X" else "X"

    def play(self) -> None:
        """
        The main game loop, prompting each player for their move, checking for a winner,
        and switching turns until someone wins or the game is terminated.
        """
        print("Welcome to Gomoku!")

        while True:
            try:
                print(f"Player {self.current_player}'s turn.")
                position = None

                # Keep rendering the board until we get a valid click/position
                while position is None:
                    position = self.display_board()

                x, y = position

                if self.place_stone(x, y):
                    if self.check_win(x, y):
                        self.display_board(winner=self.current_player)
                        print(f"Player {self.current_player} wins!")
                        break
                    self.switch_player()
                else:
                    print("Invalid move. Try again.")

            except KeyboardInterrupt:
                print("\nGame terminated.")
                break
