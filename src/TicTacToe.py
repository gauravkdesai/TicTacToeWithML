import random
import time

import numpy as np

from Board import Board
from DecisionTreeModelBuilder import DecisionTreeModelBuilder


def print_stats(match_stats, total_matches, drawn_matches):
    print()
    print()

    print("#" * 80)
    print("Final Stats")
    print("Total Matches Played in this session = {}".format(total_matches))

    for key in match_stats.keys():
        print(("Matches won by {} = {} (winning % {})".format(key, match_stats[key],
                                                              100 * match_stats[key] / total_matches)))

    print("Matches drawn = {} ({} %)".format(drawn_matches, 100 * drawn_matches / total_matches))

    print("#" * 80)


def main(number_of_iterations=1, player_config_name='RandomGuessVsHuman'):
    match_stats = {}
    total_matches = 0
    drawn_matches = 0

    for i in range(number_of_iterations):

        if i % 100 == 0 and not (i == 0):
            model_builder = DecisionTreeModelBuilder("Board_Data.csv", "Decision_Tree_Model.txt")
            model_builder.train_and_save_model()
            print_stats(match_stats, total_matches, drawn_matches)
            time.sleep(3)

        board = Board(player_config_name=player_config_name)
        print("Created board of size ", board.size)
        board.display()

        while True:

            board.play_next_player()
            board.display()

            if board.is_game_complete():
                if not board.is_draw:
                    board.winner_player_id = board.nextPlayerIndex

                break

            board.move_to_next_player()
            # time.sleep(2)

        board.display_winning_message()
        board.save()

        total_matches += 1
        if board.is_draw:
            drawn_matches += 1
        else:
            winning_player = board.players[board.winner_player_id]
            winner_name = winning_player.get_name() + " (" +  type(winning_player.player_interface).__name__+")"
            match_stats[winner_name] = match_stats.get(winner_name, 0)+1

    print_stats(match_stats, total_matches, drawn_matches)


if __name__ == "__main__":
    main(number_of_iterations=10000,player_config_name='RandomGuessVsDecisionTreePlayer')
