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
        
        return actions
    
    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def is_terminal(game_state):
        # it must return True if there is a winner or there are no more legal actions, False otherwise
        return len(ConnectFourEnvironment.get_legal_actions(game_state)) == 0\
            or ConnectFourBaseEnvironment.get_winner(game_state) is not None
    
    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def payoff(game_state, player_colour):
        # it must return a payoff for the considered player ('Y' or 'R') in a given game_state
        value = 0
        gb = game_state['game-board']
        if ConnectFourEnvironment.is_terminal(game_state):
            if ConnectFourBaseEnvironment.get_winner(game_state) == player_colour: 
             return 100
            if ConnectFourBaseEnvironment.get_winner(game_state) is not None: 
                return -100
            return 50
        
        opponent_colour = 'Y' if player_colour == 'R' else 'Y'
        openings = ConnectFourBaseEnvironment.get_openings(gb, player_colour)
        counter_openings = ConnectFourBaseEnvironment.get_openings(gb, opponent_colour)

        for opening_list in openings.values():
            for opening in opening_list:
                value += 2 if opening[1] == 2 else 5 if opening[1] == 3 else 0

        for opening_list in counter_openings.values():
            for opening in opening_list:
                if opening[1] == 2:
                    power_up = game_state['power-up-{0}'.format(opponent_colour)]
                    if power_up is not None and power_up == 'x2':
                        value -= 5
                    else:
                        value -= 2
                elif opening[1] == 3:
                    value -= 100

        return value

def connected(board, player):
    opponent_colour = 'Y' if player == 'R' else 'Y'
    lines = {
        'v': [],
        'h': [],
        'rd': [],
        'ld': []
    }
    before, pieces, after, total = 0, 0, 0, 0
    for i in range(board.get_height()):
        for j in range(board.get_width()):
            turn = board.get_item_value(j, i)
            pieces += 1 if turn == player else 0
            before += 1 if (turn == None and pieces == 0) else 0
            after += 1 if (turn == None and pieces > 0) else 0
            total += 1

            if turn == opponent_colour:
                if total >= 5 and pieces == 2:
                    lines['h'].append([i, pieces, 2])
                if total >= 5 and pieces == 3:
                    lines['h'].append([i, pieces, 100])
