from typing import List, Tuple
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

class GomokuVisualizer:
    def __init__(self, size: int = 15, cell_size: int = 50):
        self.size = size
        self.cell_size = cell_size
        self.board_img = Image.open("gomoku_board.png")
        self.black_stone = Image.open("black_stone.png").resize((cell_size, cell_size))
        self.white_stone = Image.open("white_stone.png").resize((cell_size, cell_size))
        self.current_display = None

    def render_board(self, board: List[List[str]]) -> None:
        if self.current_display:
            plt.close(self.current_display)

        board_with_pieces = self.board_img.copy()
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == "X":  # Black stone
                    position = (j * self.cell_size, i * self.cell_size)
                    board_with_pieces.paste(self.black_stone, position, self.black_stone)
                elif cell == "O":  # White stone
                    position = (j * self.cell_size, i * self.cell_size)
                    board_with_pieces.paste(self.white_stone, position, self.white_stone)

        plt.figure(figsize=(8, 8))
        plt.imshow(board_with_pieces)
        plt.axis("off")
        self.current_display = plt.gcf()
        plt.show()

class Gomoku:
    def __init__(self, size: int = 15) -> None:
        self.size = size
        self.board: List[List[str]] = [["." for _ in range(size)] for _ in range(size)]
        self.current_player: str = "X"  # X starts the game
        self.visualizer = GomokuVisualizer(size)

    def display_board(self) -> None:
        self.visualizer.render_board(self.board)

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
                x, y = map(int, input("Enter your move (row and column): ").split())
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
    # Generate necessary images if not already present
    def generate_board_image(size: int = 15, cell_size: int = 50) -> None:
        """Generate an empty Gomoku board image."""
        img_size = size * cell_size
        board = Image.new("RGB", (img_size, img_size), "burlywood")
        draw = ImageDraw.Draw(board)

        # Draw the grid
        for i in range(size):
            line_pos = i * cell_size
            draw.line([(line_pos, 0), (line_pos, img_size)], fill="black", width=1)
            draw.line([(0, line_pos), (img_size, line_pos)], fill="black", width=1)

        board.save("gomoku_board.png")
        print("Gomoku board image generated: gomoku_board.png")

    def generate_stone_image(color: str, size: int = 40) -> None:
        """Generate a Gomoku stone image."""
        stone = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(stone)
        draw.ellipse([(0, 0), (size, size)], fill=color)
        filename = f"{color}_stone.png"
        stone.save(filename)
        print(f"{color.capitalize()} stone image generated: {filename}")

    generate_board_image()
    generate_stone_image("black")
    generate_stone_image("white")

    # Start the game
    game = Gomoku()
    game.play()
