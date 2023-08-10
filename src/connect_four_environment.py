from une_ai.assignments import ConnectFourBaseEnvironment

class ConnectFourEnvironment(ConnectFourBaseEnvironment):

    def __init__(self):
        super().__init__()

    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def get_legal_actions(game_state):
        # it must return the legal actions for the current game state
        actions = []
        gb = game_state['game-board']
        for i in range(gb.get_width):
			        if ConnectFourBaseEnvironment.is_valid_column(gb, i) and !ConnectFourBaseEnvironment.is_column_full(gb, i):
                for option in  ['release-', 'popup-', 'use-power-up-']:
                    actions.append(option + i)
        return actions
    
    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def is_terminal(game_state):
        # it must return True if there is a winner or there are no more legal actions, False otherwise
        gb = 
        return False
    
    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def payoff(game_state, player_colour):
        # it must return a payoff for the considered player ('Y' or 'R') in a given game_state
        return 0