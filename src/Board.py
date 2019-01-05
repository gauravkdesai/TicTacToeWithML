import numpy as np

import Persister
from Cells import Cell
from Coputer_Interface import RandomGuess, DecisionTreePlayer
from Display import CommandLineInterface
from Players import PLAYERS_CONFIGS, PlayerSetup


class Board:
    """
    This class holds current state of TicTacToe board
    """

    def __init__(self, player_config_name, size=3, ):
        self.size = size
        self.cells = np.asarray([[Cell(row, col, size) for col in range(size)] for row in range(size)])

        self.isGameComplete = False
        self.is_draw = False
        self.winner_player_id = -1

        self.display_interface = CommandLineInterface()
        self.computer_interface = RandomGuess()
        self.decision_tree = DecisionTreePlayer()

        self.move_counter = 0 # Start from 0

        player_setup = PlayerSetup(PLAYERS_CONFIGS[player_config_name])
        self.players = player_setup.get_players()

        self.nextPlayerIndex = 0
        self.nextPlayer = self.players[self.nextPlayerIndex]

    def move_to_next_player(self):
        self.nextPlayerIndex = (self.nextPlayerIndex + 1) % (len(self.players))
        self.nextPlayer = self.players[self.nextPlayerIndex]

    def mark_cell(self, x, y):
        self.cells[x][y].set_marking = self.nextPlayer.get_marking()

    def is_game_complete(self):

        if self.isGameComplete:
            return True

        self.isGameComplete = self.check_horizontal_sequences()

        if self.isGameComplete:
            return True

        self.isGameComplete = self.check_vertical_sequences()

        if self.isGameComplete:
            return True

        self.isGameComplete = self.check_diagonal_left_to_right_sequences()

        if self.isGameComplete:
            return True

        self.isGameComplete = self.check_diagonal_right_to_left_sequences()

        if self.isGameComplete:
            return True

        if self.check_all_cells_filled():
            self.is_draw = True
            self.isGameComplete = True

        return self.isGameComplete

    def check_horizontal_sequences(self):
        for row in range(self.size):
            count_for_row = sum(
                [1 if c.is_empty() == False and c.get_marking() == self.nextPlayer.get_marking() else 0 for c in
                 self.cells[row][:]])
            if count_for_row == self.size:
                return True

        return False

    def check_vertical_sequences(self):
        for col in range(self.size):
            column = [row[col] for row in self.cells]
            count_for_column = sum(
                [1 if c.is_empty() == False and c.get_marking() == self.nextPlayer.get_marking() else 0 for c in
                 column])
            if count_for_column == self.size:
                return True

        return False

    def check_diagonal_left_to_right_sequences(self):

        count_for_major_axis = sum([
                                       1 if c.is_empty() == False
                                            and c.is_on_major_axis()
                                            and c.get_marking() == self.nextPlayer.get_marking()
                                       else 0
                                       for c2 in self.cells[:][:] for c in c2])
        if count_for_major_axis == self.size:
            return True

        return False

    def check_diagonal_right_to_left_sequences(self):
        count_for_minor_axis = sum([
                                       1 if c.is_empty() == False
                                            and c.is_on_minor_axis()
                                            and c.get_marking() == self.nextPlayer.get_marking()
                                       else 0
                                       for c2 in self.cells[:][:] for c in c2])
        if count_for_minor_axis == self.size:
            return True

        return False

    def display(self):
        self.display_interface.display_board(self)

    def play_next_player(self):

        attempt_counter = 0
        MAX_ATTEMPTS = 10

        while True:

            if attempt_counter >= MAX_ATTEMPTS:
                print("Crossed allowed attempts to make a move. Passing to next player", attempt_counter, MAX_ATTEMPTS)
                break;

            x, y = self.nextPlayer.player_interface.get_next_move(self)

            # print("User Move ",x,y)
            to_be_marked_cell = self.cells[x][y]
            if to_be_marked_cell.is_empty():
                self.move_counter += 1
                to_be_marked_cell.set_marking(self.nextPlayer.get_marking(), self.move_counter)
                # print(to_be_marked_cell)
                #self.display_interface.display_player_made_move_message(self)
                break

            attempt_counter += 1

    def display_winning_message(self):
        self.display_interface.display_winning_message(self)

    def check_all_cells_filled(self):
        count_for_entire_board = sum([1 if c.is_empty() == False else 0 for c2 in self.cells[:][:] for c in c2])
        if count_for_entire_board == self.size ** 2:
            return True

        return False

    def save(self):
        persister = Persister.CSVWriter(self)
        persister.persist_board()