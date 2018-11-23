from Markings import Marking

CELL_NOT_MARKED = -1 # Default indicating not marked


class CellPosition:
    def __init__(self, x, y, board_size):
        self.x = x
        self.y = y
        self.boardSize = board_size
        self.normalizedPosition = (board_size * x) + y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_board_size(self):
        return self.boardSize

    def get_normalized_position(self):
        return self.normalizedPosition


class Cell:
    """
    This class hold information about TicTacTo Cell
    """

    def __init__(self, x, y, board_size):
        self.marking = Marking() # Initialize with empty Marking
        self.isEmpty = True
        self.position = CellPosition(x, y, board_size)
        self.isOnMajorAxis = (x == y)
        self.isOnMinorAxis = ((x + y) == (board_size - 1))
        self.markingSequence = CELL_NOT_MARKED

    def set_marking(self, marking, move_counter=-1):
        self.marking = marking
        self.isEmpty = False
        self.markingSequence = move_counter

    def get_marking(self):
        return self.marking

    def get_marking_character(self):
        return self.marking.get_character()

    def is_empty(self):
        return self.isEmpty

    def get_position(self):
        return self.position

    def is_on_major_axis(self):
        return self.isOnMajorAxis

    def is_on_minor_axis(self):
        return self.isOnMinorAxis

    def get_marking_sequence(self):
        return self.markingSequence
