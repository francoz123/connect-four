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
        power_up = game_state['power-up-' + player]
        for i in range(gb.get_width()):
            if ConnectFourBaseEnvironment.is_valid_column(gb, i) and not ConnectFourBaseEnvironment.is_column_full(gb, i)\
                and ConnectFourBaseEnvironment.get_first_free_row(gb, i) is not None:
                actions.append('release-{0}'.format(i))
                if power_up is not None:
                    actions.append('use-power-up-{0}'.format(i))
                if gb.get_item_value(i, gb.get_height()-1) == player:
                    actions.append('popup-{0}'.format(i))
            elif ConnectFourBaseEnvironment.is_valid_column(gb, i) and power_up is not None and power_up == 'anvil':
                actions.append('use-power-up-{0}'.format(i))
        print(actions)
        return actions
    
    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def is_terminal(game_state):
        # it must return True if there is a winner or there are no more legal actions, False otherwise
        return ConnectFourBaseEnvironment.get_legal_actions(game_state) is not None\
            or ConnectFourBaseEnvironment.get_winner(game_state) is not None
    
    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def payoff(game_state, player_colour):
        # it must return a payoff for the considered player ('Y' or 'R') in a given game_state
        if ConnectFourBaseEnvironment.get_winner(game_state) == player_colour: 
             return 1 
        if ConnectFourBaseEnvironment.get_winner(game_state) is not None: 
             return -1 
        return 0