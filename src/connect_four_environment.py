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
        opponent_colour = 'Y' if player_colour == 'R' else 'R'
        value = 0
        gb = game_state['game-board']
        if ConnectFourEnvironment.is_terminal(game_state):
            if ConnectFourBaseEnvironment.get_winner(game_state) == player_colour: 
             return 200
            if ConnectFourBaseEnvironment.get_winner(game_state) is not None: 
                return -200
            return 100
        openings = [horizontals(gb, player_colour), right_diagonals(gb, player_colour), left_diagonals(gb, player_colour)]
        verticals = ConnectFourBaseEnvironment.get_openings(gb, player_colour)['verticals']
        counter_openings = [horizontals(gb, player_colour), right_diagonals(gb, player_colour), left_diagonals(gb, player_colour)]
        counter_vert = ConnectFourBaseEnvironment.get_openings(gb, opponent_colour)['verticals']

        for col in verticals:
            if col[1] == 2:
                if game_state['power-up-{0}'.format(opponent_colour)] == 'x2':
                    return -200
                value += 2
            elif col[1] == 3:
                value += 5

        for col in counter_vert:
            if col[1] == 2:
                value -= 2
            elif col[1] == 3:
                return -200

        for opening_list in openings:
            for opening in opening_list:
                value += 2*opening['twos']
                if len(opening['threes']) > 0:
                    for item in opening['threes']:
                        value += 5

        for opening_list in counter_openings:
            for opening in opening_list:
                value -= 2*opening['twos']
                if len(opening['threes']) > 0:
                    for item in opening['threes']:
                        if item['can-win']:
                            return -200
                        else:
                            value -= 5


        return value

def horizontals(board, player):
    opponent_colour = 'Y' if player == 'R' else 'R'
    openings = []
    # Calculate horizontal twos
    for row in range(board.get_height()):
        twos, threes = 0, []
        for col in range(board.get_width()-3):
            start, stop, pieces, gaps = col, col + 3, [], []
            while start <= stop and board.get_item_value(start, row) != opponent_colour:
                if board.get_item_value(start, row) == player:
                    pieces += 1 
                else:
                    gaps.append(start)
                start += 1
            if start == stop + 1:
                if pieces == 2:
                    if (row == 5 and board.get_item_value(gaps[0], row) is None and board.get_item_value(gaps[1], row) is None) or\
                        (row < 5 and board.get_item_value(gaps[0], row+1) is not None and board.get_item_value(gaps[1], row+1) is not None):
                        twos.append({'can-win':True, 'opening':gaps})
                    else:
                        twos.append({'can-win':False, 'opening':gaps})
                if pieces == 3:
                    if (row == 5  and board.get_item_value(gaps[0], row) is None) or\
                        (row < 5 and board.get_item_value(gaps[0], row+1) is None):
                        threes.append({'can-win':True, 'opening':gaps[0]})
                    else:
                        threes.append({'can-win':False, 'opening':gaps[0]})
        if len(twos) > 0 or len(threes) > 0:
            openings.append({'number': row, 'twos': twos,'threes': threes})
    return openings

def right_diagonals(board, player):
    opponent_colour = 'Y' if player == 'R' else 'R'
    openings = []
    end = 3
    number = 3
    for col in range(end + 1):
        for row in ([0] if col > 0 else range(3)):
            twos, threes = [], []
            x, y,  = col, row
            col_end = 5-y if x < 1 else 6
            row_end = 5 if x <= 1 else 6-x
            stop_col = col_end-3
            stop_row = 2 if x <= 1 else 1 if x == 2 else 0
            #print('st', col, row, 'end', col_end, row_end, 'stp', stop_col, stop_row)
            while x <= stop_col and y <= stop_row:
                pieces = 0
                start_x, start_y, stop, gaps = x, y, x + 3, []
                while start_x <= stop and board.get_item_value(start_x, start_y) != opponent_colour:
                    if board.get_item_value(start_x, start_y) == player:
                        pieces += 1 
                    else:
                        gaps.append([start_y, start_x])
                    start_x += 1
                    start_y += 1
                if start_x == stop + 1:
                    if pieces == 2:
                        twos.append({'can-win':False, 'opening':[gaps[0][1], gaps[1][1]]}) 
                    if pieces == 3:
                        if (gaps[0][0] == 0 and board.get_item_value(gaps[0][1], gaps[0][0]) is None) or\
                              (gaps[0][0] < 5 and board.get_item_value(gaps[0][1], gaps[0][0]+1) is not None):
                            threes.append({'can-win':True, 'opening':gaps[0][1]})
                        else:
                            threes.append({'can-win':False, 'opening':gaps[0][1]})
                x, y = x+1, y+1
            if twos > 0 or len(threes) > 0:
                openings.append({'number': number, 'twos': twos,'threes': threes})
            number += 1
        

    return openings
    
def left_diagonals(board, player):
    opponent_colour = 'Y' if player == 'R' else 'R'
    openings = []
    end = 3
    number = 4
    # Calculate horizontal twos
    for col in range(end + 1):
        for row in ([5] if col > 0 else range(3,6)):
            twos, threes = 0, []
            x, y,  = col, row
            col_end = 5+y if x < 1 else 6
            row_end = 0 if x <= 1 else x-1
            stop_col = col_end-3
            stop_row = 3 if x <= 1 else 4 if x == 2 else 5
            #print('st', col, row, 'end', col_end, row_end, 'stp', stop_col, stop_row)
            while x <= stop_col and y >= stop_row:
                pieces = 0
                start_x, start_y, stop, gaps = x, y, x + 3, []
                while start_x <= stop and board.get_item_value(start_x, start_y) != opponent_colour:
                    if board.get_item_value(start_x, start_y) == player:
                        pieces += 1 
                    else:
                        gaps.append([start_y, start_x])
                    start_x += 1
                    start_y -= 1
                if start_x == stop + 1:
                    if pieces == 2:
                        twos.append({'can-win':False, 'opening':[gaps[0][1], gaps[1][1]]}) 
                    if pieces == 3:
                        if (gaps[0][0] == 5 and board.get_item_value(gaps[0][1], gaps[0][0]) is None) or\
                            (gaps[0][0] < 5 and board.get_item_value(gaps[0][1], gaps[0][0]+1) is not None):
                            threes.append({'can-win':True, 'opening':gaps[0][1]})
                        else:
                            threes.append({'can-win':False, 'opening':gaps[0][1]})
                x, y = x+1, y-1
            if twos > 0 or len(threes) > 0:
                openings.append({'number': number, 'twos': twos,'threes': threes})
            number += 1
        

    return openings