from typing import List, Tuple
import pytest
from gomoku.game import Gomoku

@pytest.fixture
def near_win_game() -> Gomoku:
    """Fixture to create a game where a player is one move away from winning."""
    game: Gomoku = Gomoku()
    for i in range(4):  # Place 4 stones in a row for player X
        game.place_stone(0, i)
    return game

@pytest.fixture
def mixed_board_game() -> Gomoku:
    """Fixture to create a game with a mixed board state."""
    game: Gomoku = Gomoku()
    moves: List[Tuple[int, int, str]] = [
        (0, 0, "X"), (0, 1, "O"),
        (1, 1, "X"), (1, 2, "O"),
        (2, 2, "X"), (2, 3, "O"),
        (3, 3, "X")
    ]
    for x, y, player in moves:
        game.current_player = player
        game.place_stone(x, y)
    game.current_player = "X"  # Ensure it's X's turn
    return game

@pytest.fixture
def diagonal_near_win() -> Gomoku:
    """Fixture to set up a game where a diagonal win is one move away."""
    game: Gomoku = Gomoku()
    for i in range(4):
        game.place_stone(i, i)
    return game

def test_board_initialization() -> None:
    game: Gomoku = Gomoku()
    assert len(game.board) == 15
    assert all(len(row) == 15 for row in game.board)
    assert all(cell == "." for row in game.board for cell in row)

def test_near_win_horizontal(near_win_game: Gomoku) -> None:
    assert near_win_game.place_stone(0, 4) is True
    assert near_win_game.check_win(0, 4) is True

def test_mixed_board_state(mixed_board_game: Gomoku) -> None:
    assert mixed_board_game.is_valid_move(0, 2) is True
    assert mixed_board_game.place_stone(0, 2) is True
    assert mixed_board_game.board[0][2] == "X"

def test_switch_player(mixed_board_game: Gomoku) -> None:
    assert mixed_board_game.current_player == "X"
    mixed_board_game.switch_player()
    assert mixed_board_game.current_player == "O"

def test_diagonal_win(diagonal_near_win: Gomoku) -> None:
    assert diagonal_near_win.place_stone(4, 4) is True
    assert diagonal_near_win.check_win(4, 4) is True

def test_no_win_yet(mixed_board_game: Gomoku) -> None:
    assert not mixed_board_game.check_win(3, 3)

def test_invalid_moves(mixed_board_game: Gomoku) -> None:
    assert mixed_board_game.is_valid_move(0, 0) is False
    assert mixed_board_game.is_valid_move(-1, -1) is False
    assert mixed_board_game.is_valid_move(15, 15) is False

def test_place_and_win(near_win_game: Gomoku) -> None:
    assert near_win_game.place_stone(0, 4) is True
    assert near_win_game.check_win(0, 4) is True

