import csv
from operator import itemgetter


def get_score(current_player_is_winner, distance_to_last_move, is_draw):
    if is_draw:
        total_points = 2
    else:
        total_points = 15

    score = total_points #- distance_to_last_move

    if (not is_draw) and (not current_player_is_winner):
        score *= -1

    return score


class CSVWriter:
    def __init__(self, board):
        self.filePath = "Board_Data.csv"
        self.board = board

    def persist_board(self):
        board_lines = self.convert_to_list()

        with open(self.filePath, "a+") as fileToWrite:
            fileWriter = csv.writer(fileToWrite)
            fileWriter.writerows(board_lines)

        #print("Board persisted in {} file".format(self.filePath))

    def clear(self):
        pass

    def convert_to_list(self):
        winner_player_index = self.board.winner_player_id
        is_draw = self.board.is_draw
        board_size = self.board.size

        board_info = [(c.markingSequence, board_size * c.position.get_x() + c.position.get_y()) for c2 in
                      self.board.cells[:][:] for c in c2 if c.markingSequence != -1]

        '''for cell_info in board_info:
            print(cell_info[0],cell_info[1])'''

        board_info = sorted(board_info, key=itemgetter(0))
        #print("After sorting by move sequence")
        board_info_to_save = []
        current_player_is_winner = (0 == winner_player_index)
        moves = ""
        for (cell_sequence, current_move) in board_info:
            #print(cell_sequence, current_move)

            distance_to_last_move = len(board_info) - cell_sequence
            score = get_score(current_player_is_winner, distance_to_last_move, is_draw)

            board_info_row = [moves, current_move, score]
            board_info_to_save.append(board_info_row)

            current_player_is_winner = not (current_player_is_winner)
            moves += str(current_move)

        return board_info_to_save
