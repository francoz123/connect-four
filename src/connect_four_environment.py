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
        player = game_state['player-turn']
        for i in range(gb.get_width):
	if ConnectFourBaseEnvironment.is_valid_column(gb, i) and !ConnectFourBaseEnvironment.is_column_full(gb, i):
	for option in  ['release-', 'use-power-up-']:
		actions.append(option + i)
	if gb.get_item_value(i, 0) == player:
		actions.append('popup-{0}'.format(i))
        return actions
    
    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def is_terminal(game_state):
        # it must return True if there is a winner or there are no more legal actions, False otherwise
        return len(ConnectFourBaseEnvironment.get_legal_action(game_state)) == 0 or ConnectFourBaseEnvironment.get_winner(game_state) is not None
    
    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def payoff(game_state, player_colour):
        # it must return a payoff for the considered player ('Y' or 'R') in a given game_state
        if ConnectFourBaseEnvironment.get_winner(game_state) == player_name: 
             return 1 
        if ConnectFourBaseEnvironment.get_winner(game_state) is not None: 
             return -1 
        return 0