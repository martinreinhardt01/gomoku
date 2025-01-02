from gomoku import Gomoku
from gomoku import GomokuVisualizer, generate_stone_image

if __name__ == "__main__":
    board_size = 15

    # Generate necessary images if not already present
    generate_stone_image("black")
    generate_stone_image("white")

    # Create a visualizer and inject it into the Gomoku game
    visualizer = GomokuVisualizer(size=board_size)
    game = Gomoku(size=board_size, visualizer=visualizer)

    # Start the game
    game.play()
