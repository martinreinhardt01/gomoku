from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backend_bases import Event

class Visualizer(ABC):
    @abstractmethod
    def display_board(self, board: List[List[str]], winner: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def get_next_position(self) -> Tuple[int, int]:
        pass

class GomokuVisualizer(Visualizer):
    def __init__(self, size: int = 15, cell_size: int = 50):
        self.size = size
        self.cell_size = cell_size
        self.board_img = self.generate_board_image(size)
        self.black_stone = self.load_or_generate_stone_image("black")
        self.white_stone = self.load_or_generate_stone_image("white")
        self.clicked_position: Optional[Tuple[int, int]] = None

    def load_or_generate_stone_image(self, color: str) -> Image.Image:
        filename = f"{color}_stone.png"
        try:
            return Image.open(filename).resize((self.cell_size, self.cell_size))
        except FileNotFoundError:
            return self.generate_stone_image(color)

    def generate_stone_image(self, color: str) -> Image.Image:
        stone = Image.new("RGBA", (self.cell_size, self.cell_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(stone)
        draw.ellipse([(0, 0), (self.cell_size, self.cell_size)], fill=color)
        filename = f"{color}_stone.png"
        stone.save(filename)
        print(f"{color.capitalize()} stone image generated: {filename}")
        return stone

    def generate_board_image(self, size: int) -> Image.Image:
        img_size = size * self.cell_size
        board = Image.new("RGB", (img_size, img_size), "burlywood")
        draw = ImageDraw.Draw(board)
        for i in range(size):
            line_pos = i * self.cell_size
            draw.line([(line_pos, 0), (line_pos, img_size)], fill="black", width=1)
            draw.line([(0, line_pos), (img_size, line_pos)], fill="black", width=1)
        return board

    def display_board(self, board: List[List[str]], winner: Optional[str] = None) -> None:
        self.clicked_position = None
        board_with_pieces = self.board_img.copy()
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == "X":
                    position = (j * self.cell_size, i * self.cell_size)
                    board_with_pieces.paste(self.black_stone, position, self.black_stone)
                elif cell == "O":
                    position = (j * self.cell_size, i * self.cell_size)
                    board_with_pieces.paste(self.white_stone, position, self.white_stone)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(board_with_pieces)
        ax.axis("off")

        if winner:
            ax.text(
                self.size * self.cell_size // 2, 
                self.size * self.cell_size + 10,
                f"Player {winner} wins!",
                color="red", fontsize=20, ha="center"
            )

        def on_click(event: Event) -> None:
            if not winner and hasattr(event, "xdata") and hasattr(event, "ydata"):
                if event.xdata is not None and event.ydata is not None:
                    x = int(event.ydata // self.cell_size)
                    y = int(event.xdata // self.cell_size)
                    self.clicked_position = (x, y)
                    plt.close(fig)

        fig.canvas.mpl_connect("button_press_event", on_click)
        plt.show()

    def get_next_position(self) -> Tuple[int, int]:
        return self.clicked_position

class TerminalVisualizer(Visualizer):
    def display_board(self, board: List[List[str]], winner: Optional[str] = None) -> None:
        for row in board:
            print(" ".join(row))
        if winner:
            print(f"Player {winner} wins!")

    def get_next_position(self) -> Tuple[int, int]:
        x = int(input("Enter the row: "))
        y = int(input("Enter the column: "))
        return x, y