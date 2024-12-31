from gomoku import Gomoku

if __name__ == "__main__":
    Gomoku.generate_board_image()
    Gomoku.generate_stone_image("black")
    Gomoku.generate_stone_image("white")

    game = Gomoku(size=15)
    game.play()
