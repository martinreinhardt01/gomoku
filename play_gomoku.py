from gomoku import Gomoku

if __name__ == "__main__":
    board_size = 15

    # Generate necessary images
    Gomoku.generate_stone_image("black")
    Gomoku.generate_stone_image("white")

    # Start the game
    game = Gomoku(size=board_size)
    game.play()