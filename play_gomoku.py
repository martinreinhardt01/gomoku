from gomoku import Gomoku
from gomoku.visualizer import GomokuVisualizer, TerminalVisualizer

if __name__ == "__main__":
    board_size = 15
    visualizer = GomokuVisualizer(size=board_size)
    game = Gomoku(size=board_size, visualizer=visualizer)
    game.play()