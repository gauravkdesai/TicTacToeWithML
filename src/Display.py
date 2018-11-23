from Coputer_Interface import PlayerInterface


class DisplayInterface:

    def display_board(self): pass

    def display_winning_message(self): pass

    def display_player_made_move_message(self): pass


class CommandLineInterface(DisplayInterface, PlayerInterface):
    def display_board(self, board):
        print('\r\r')
        print("TicTacToe - Board after {} moves".format(board.move_counter))

        print("_" * (board.size * 2 + 1))

        for r in range(board.size):
            # print('Row=',r)
            print("|", end="")
            for c in board.cells[r][:]:
                print(c.get_marking_character() + "|", end=""),
            print()
            print("-" * (board.size * 2 + 1))

    def display_winning_message(self, board):

        if board.is_draw:
            print("Game ended in draw.")
        else:

            if board.nextPlayer.isHuman:
                print("Congratulations '{0}', you won!!!".format(board.nextPlayer.name))
            else:
                print("You lost. Better luck next time!!")

    def get_next_move(self, board):
        while True:
            input_string = input("Enter your move between 1 to 9:")
            if input_string.isdigit():
                break
            else:
                print("{0} is invalid option, please choose your move between 1 to 9".format(input_string))

        position = int(input_string)

        x = int((position - 1) / board.size)
        y = int((position - 1) % board.size)

        return (x, y)

    def display_player_made_move_message(self, board):
        name = board.nextPlayer.name
        print('*' * 40)
        print("{} made move ({})".format(name, board.nextPlayer.marking.get_character()))
