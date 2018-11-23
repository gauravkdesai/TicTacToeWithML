import random
from operator import itemgetter

import numpy as np

from Cells import CELL_NOT_MARKED
from DecisionTreeModelBuilder import DecisionTreeModelBuilder


class PlayerInterface:

    def get_next_move(self, board): pass


class ComputerInterface(PlayerInterface):
    def get_next_move(self, board): pass


class RandomGuess(ComputerInterface):
    def get_next_move(self, board):
        empty_cells = [c for c2 in board.cells for c in c2 if c.is_empty()]
        # print("Empty cells=",len(empty_cells))

        random_move_cell_id = random.randint(0, len(empty_cells) - 1)
        selected_position = empty_cells[random_move_cell_id].get_position()
        return selected_position.get_x(), selected_position.get_y()


class DecisionTreePlayer(ComputerInterface):
    def __init__(self):
        self.model_builder = DecisionTreeModelBuilder("Board_Data.csv", "Decision_Tree_Model.txt")

    def get_next_move(self, board):
        board_info = [(c.markingSequence, c.get_position().get_normalized_position()) for c2 in
                      board.cells[:][:] for c in c2 if c.markingSequence != CELL_NOT_MARKED]
        board_info = sorted(board_info, key=itemgetter(0))

        board_state = "".join([str(move) for seq, move in board_info])
        print('board_state=', board_state)

        # get score for each of the empty cell
        empty_cells = np.asarray(
            [c for c2 in board.cells[:][:] for c in c2 if
             c.markingSequence == -1])
        scores = np.full(empty_cells.shape, -100)
        print('scores length', scores.shape)
        print('empty_cells length', empty_cells.shape)

        for index, empty_cell in np.ndenumerate(empty_cells):
            cell_normalized_location = empty_cell.get_position().get_normalized_position()
            scores[index] = self.model_builder.get_next_move_score(board_state, cell_normalized_location)

            print(
                "For for current board state {}, index {}, for next move cell {} score is {}".format(board_state, index,
                                                                                                     cell_normalized_location,
                                                                                                     scores[index]))

        max_score_index_list = np.argwhere(scores == np.max(scores))
        max_score_index_list = max_score_index_list.flatten().tolist()


        max_score_index = random.choice(max_score_index_list) # pick random max score index
        print("Maximum score {} for move {} at index {}".format(scores[max_score_index], empty_cells[max_score_index],
                                                                max_score_index))

        next_move_x = empty_cells[max_score_index].position.get_x()
        next_move_y = empty_cells[max_score_index].position.get_y()

        print('x={}, y={}'.format(next_move_x, next_move_y))

        return next_move_x, next_move_y
