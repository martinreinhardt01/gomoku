from typing import List, Optional, Tuple
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backend_bases import Event

class GomokuVisualizer:
    def __init__(self, size: int = 15, cell_size: int = 50):
        """
        Responsible for handling all rendering of the board and stones,
        as well as capturing clicks from the user.
        """
        self.size = size
        self.cell_size = cell_size
        self.board_img = self.generate_board_image(size)
        self.black_stone = Image.open("black_stone.png").resize((cell_size, cell_size))
        self.white_stone = Image.open("white_stone.png").resize((cell_size, cell_size))

        # clicked_position can be None until the user clicks on the board
        self.clicked_position: Optional[Tuple[int, int]] = None

    def generate_board_image(self, size: int) -> Image.Image:
        """Generate an empty Gomoku board image."""
        img_size = size * self.cell_size
        board = Image.new("RGB", (img_size, img_size), "burlywood")
        draw = ImageDraw.Draw(board)

        # Draw the grid
        for i in range(size):
            line_pos = i * self.cell_size
            draw.line([(line_pos, 0), (line_pos, img_size)], fill="black", width=1)
            draw.line([(0, line_pos), (img_size, line_pos)], fill="black", width=1)

        return board

    def render_board(
        self,
        board: List[List[str]],
        winner: Optional[str] = None
    ) -> Optional[Tuple[int, int]]:
        """
        Renders the current board state with stones in place.
        If `winner` is provided, displays a message on top.
        Captures the user's next click and returns its (x, y) position on the grid.
        Returns None if the window closes without a click.
        """
        self.clicked_position = None

        board_with_pieces = self.board_img.copy()
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == "X":  # Black stone
                    position = (j * self.cell_size, i * self.cell_size)
                    board_with_pieces.paste(self.black_stone, position, self.black_stone)
                elif cell == "O":  # White stone
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
                    x = int(event.ydata // self.cell_size)  # convert click to row
                    y = int(event.xdata // self.cell_size)  # convert click to column
                    self.clicked_position = (x, y)
                    plt.close(fig)

        fig.canvas.mpl_connect("button_press_event", on_click)
        plt.show()

        return self.clicked_position


def generate_stone_image(color: str, size: int = 40) -> None:
    """
    Generates a Gomoku stone image of the given color and size, saved as `{color}_stone.png`.
    """
    stone = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stone)
    draw.ellipse([(0, 0), (size, size)], fill=color)
    filename = f"{color}_stone.png"
    stone.save(filename)
    print(f"{color.capitalize()} stone image generated: {filename}")
