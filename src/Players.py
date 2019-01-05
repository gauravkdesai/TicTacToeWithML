from Coputer_Interface import RandomGuess, ComputerInterface, DecisionTreePlayer, BasicRules
from random import shuffle

from Display import CommandLineInterface
from Markings import X, O


class Player:
    """
    class to hold player info
    """

    def __init__(self, name, marking, player_interface):
        self.name = name
        self.marking = marking
        self.isHuman = not (isinstance(player_interface, ComputerInterface))
        self.player_interface = player_interface

    def get_name(self):
        return self.name

    def get_marking(self):
        return self.marking

    def is_human(self):
        return self.isHuman

    def get_player_interface(self):
        return self.player_interface

    def set_marking(self, marking):
        self.marking = marking


PLAYER_A_DEFAULT_NAME = "Proton"
PLAYER_B_DEFAULT_NAME = "Electron"
PLAYER_A_DEFAULT_INTERFACE = RandomGuess()
PLAYER_B_DEFAULT_INTERFACE = RandomGuess()


class PlayerSetup:
    """
    Class holds Player factory methods to setup players at start of game
    """

    def __init__(self, player_setup_config):
        self.players = []
        self.player_setup_config = player_setup_config

        self.setup_a_players()

    def get_players(self):
        return self.players

    def get_player(self, index):
        '''
        return player - index 0 indicates first player, 1 indicates second player
        '''
        return self.players[index]

    def setup_a_players(self):
        # Extract configurations passed in
        player_A_name = self.player_setup_config.get('player1').get('name',PLAYER_A_DEFAULT_NAME)
        player_A_interface = self.player_setup_config.get('player1').get('interface')

        player_B_name = self.player_setup_config.get('player2').get('name',PLAYER_B_DEFAULT_NAME)
        player_B_interface = self.player_setup_config.get('player2').get('interface')

        maintain_order = self.player_setup_config['maintain_order']

        # Fill in any missing information as not all configuration is compulsory
        if player_A_interface is None:
            player_A_interface = PLAYER_A_DEFAULT_INTERFACE

        if player_B_interface is None:
            player_B_interface = PLAYER_B_DEFAULT_INTERFACE

        if maintain_order is None:
            maintain_order = True

        # Create players with available info
        self.players.append(Player(player_A_name, X(), player_A_interface))
        self.players.append(Player(player_B_name, O(), player_B_interface))

        # If we have to randomize the order of playing then shuffle the list but reset the markign
        # so that first player to play always starts with X
        if not maintain_order:
            shuffle(self.players)
            self.players[0].set_marking(X())
            self.players[1].set_marking(O())


PLAYERS_CONFIGS = \
    {
        'HumanVsHuman-RandomOrder':
            {
                'player1': {'interface': CommandLineInterface()},
                'player2': {'interface': CommandLineInterface()},
                'maintain_order': False
            },
        'HumanVsHuman':
            {
                'player1': {'interface': CommandLineInterface()},
                'player2': {'interface': CommandLineInterface()},
                'maintain_order': True
            },
        'RandomGuessVsHuman':
            {
                'player1': {'interface': CommandLineInterface()},
                'player2': {'interface': RandomGuess()},
                'maintain_order': False
            },
        'RandomGuessVsRandomGuess':
            {
                'player1': {'interface': RandomGuess()},
                'player2': {'interface': RandomGuess()},
                'maintain_order': False
            },
        'RandomGuessVsDecisionTreePlayer':
            {
                'player1': {'interface': RandomGuess()},
                'player2': {'interface': DecisionTreePlayer()},
                'maintain_order': False
            },
        'DecisionTreePlayerVsDecisionTreePlayer':
            {
                'player1': {'interface': DecisionTreePlayer()},
                'player2': {'interface': DecisionTreePlayer()},
                'maintain_order': False
            },
        'HumanVsDecisionTreePlayer-RandomOrder':
            {
                'player1': {'interface': CommandLineInterface()},
                'player2': {'interface': DecisionTreePlayer()},
                'maintain_order': False
            },
        'BasicRulesVsDecisionTreePlayer':
            {
                'player1': {'interface': BasicRules()},
                'player2': {'interface': DecisionTreePlayer()},
                'maintain_order': False
            },
        'BasicRulesVsHuman-RandomOrder':
            {
                'player1': {'interface': BasicRules()},
                'player2': {'interface': CommandLineInterface()},
                'maintain_order': False
            }




    }
