import unittest

from TicTacToe import O
from Board import Board
from Markings import X, O


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.x = X()
        self.o = O()

    def test_first_row_complete_X(self):
        board = Board(random_marker=False)
        board.cells[0][0].set_marking(self.x)
        board.cells[0][1].set_marking(self.x)
        board.cells[0][2].set_marking(self.x)
        board.cells[1][0].set_marking(self.o)
        board.cells[1][1].set_marking(self.o)

        self.assertTrue(board.is_game_complete())

    def test_first_row_complete_O(self):
        board = Board(random_marker=False)
        board.cells[0][0].set_marking(self.o)
        board.cells[0][1].set_marking(self.o)
        board.cells[0][2].set_marking(self.o)
        board.cells[1][0].set_marking(self.x)
        board.cells[1][1].set_marking(self.x)
        board.cells[2][1].set_marking(self.x)
        board.move_to_next_player()

        self.assertTrue(board.is_game_complete())

    def test_second_column_complete_X(self):
        board = Board(random_marker=False)
        board.cells[0][1].set_marking(self.x)
        board.cells[1][1].set_marking(self.x)
        board.cells[2][1].set_marking(self.x)
        board.cells[1][0].set_marking(self.o)
        board.cells[2][2].set_marking(self.o)

        self.assertTrue(board.is_game_complete())

    def test_second_major_axis_complete_X(self):
        board = Board(random_marker=False)
        board.cells[0][0].set_marking(self.x)
        board.cells[1][1].set_marking(self.x)
        board.cells[2][2].set_marking(self.x)
        board.cells[1][0].set_marking(self.o)
        board.cells[2][0].set_marking(self.o)

        self.assertTrue(board.is_game_complete())

    def test_second_minor_axis_complete_X(self):
        board = Board(random_marker=False)
        board.cells[0][2].set_marking(self.x)
        board.cells[1][1].set_marking(self.x)
        board.cells[2][0].set_marking(self.x)
        board.cells[1][0].set_marking(self.o)
        board.cells[2][2].set_marking(self.o)

        self.assertTrue(board.is_game_complete())

    def test_draw_X(self):
        board = Board(random_marker=False)
        board.cells[0][0].set_marking(self.x)
        board.cells[0][1].set_marking(self.o)
        board.cells[0][2].set_marking(self.x)
        board.cells[1][0].set_marking(self.o)
        board.cells[1][1].set_marking(self.x)
        board.cells[1][2].set_marking(self.x)
        board.cells[2][0].set_marking(self.o)
        board.cells[2][1].set_marking(self.x)
        board.cells[2][2].set_marking(self.o)

        self.assertTrue(board.is_game_complete())
        self.assertTrue(board.is_draw)


if __name__ == '__main__':
    unittest.main()
