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
        h = horizontals(gb, player_colour)
        print('HORIZONTALS', h)
        opponent_colour = 'Y' if player_colour == 'R' else 'Y'
        openings = ConnectFourBaseEnvironment.get_openings(gb, player_colour)
        counter_openings = ConnectFourBaseEnvironment.get_openings(gb, opponent_colour)

        for opening_list in openings.values():
            for opening in opening_list:
                value += 2 if opening[1] == 2 else 5 if opening[1] == 3 else 0

        for opening_list in counter_openings.values():
            for opening in opening_list:
                if opening[1] == 2:
                    """ power_up = game_state['power-up-{0}'.format(opponent_colour)]
                    if power_up is not None and power_up == 'x2':
                        value -= 5
                    else: """
                    value -= 2
                elif opening[1] == 3:
                    value -= 100

        return value

def horizontals(board, player):
    opponent_colour = 'Y' if player == 'R' else 'R'
    openings = []
    # Calculate horizontal twos
    for row in range(board.get_height()):
        twos, threes = 0, []
        for col in range(board.get_width()-3):
            start, stop, gaps = col, col + 3, []
            pieces = 0
            while (start <= stop and board.get_item_value(start, row) != opponent_colour):
                #print('s: {0}, player: {1}, item: {2}, pieces: {3}, row: {4}'.format(start, player, board.get_item_value(start, row), pieces, row))
                if board.get_item_value(start, row) == player:
                    pieces += 1 
                else:
                    gaps.append(start)
                start += 1
            if start == stop + 1:
                if pieces == 2:
                    twos += 1 
                if pieces == 3:
                    print('PG: {0}, {1}'.format(pieces, gaps))
                    if row == 0 or (row > 0 and board.get_item_value(gaps[0], row-1) is not None):
                        threes.append([row, True, gaps[0]])
                    else:
                        threes.append([row, False, gaps[0]])
            pieces = 0

        if twos > 0 or len(threes) > 0:
            openings.append([row, {'twos': twos,'threes': threes}])
    return openings

def right_diagonals(board, player):
    opponent_colour = 'Y' if player == 'R' else 'Y'
    openings = []
    end = 3
    # Calculate horizontal twos
    for col in range(end + 1):
        for row in (range(5, 6) if col > 0 else range(3, 6)):
            twos, threes = 0, []
            x, y,  = col, row
            col_end, row_end = 6-(6-y), 0
            stop_col, stop_row = col_end-3, y-(y-3)
            while x <= stop_col and y >= stop_row:
                pieces = 0
                start_x, start_y, stop, gaps = x, y, x + 3, []
                while start_x <= stop and not (board.get_item_value(start_x, start_y) == opponent_colour):
                    if board.get_item_value(start_x, start_y) == player:
                        pieces += 1 
                    else:
                        gaps.append([start_x, start_y])
                    start_x += 1
                    start_y -= 1
                if start_x == stop:
                    if pieces == 2:
                        twos += 1 
                    if pieces == 3:
                        if (gaps[0][1] == 0 and board.get_item_value(gaps[0][0], gaps[0][1]) is None) or\
                              (gaps[0][1] > 0 and board.get_item_value(gaps[0][0], gaps[0][1]-1) is not None):
                            threes.append([row, True, gaps[0][0]])
                        else:
                            threes.append([row, False, gaps[0][0]])
                x, y = x+1, y-1
        if twos > 0 or len(threes) > 0:
            openings.append([row, {'twos': twos,'threes': threes}])

    return openings

def left_diagonals(board, player):
    opponent_colour = 'Y' if player == 'R' else 'Y'
    openings = []
    end = 3
    # Calculate horizontal twos
    for col in range(end + 1):
        for row in (range(1) if col > 0 else range(3)):
            twos, threes = 0, []
            x, y,  = col, row
            col_end, row_end = 6-(6-y), 5
            stop_col, stop_row = col_end-3, y+(y-2)
            while x <= stop_col and y <= stop_row:
                pieces = 0
                start_x, start_y, stop, gaps = x, y, x + 3, []
                while start_x <= stop and not (board.get_item_value(start_x, start_y) == opponent_colour):
                    if board.get_item_value(start_x, start_y) == player:
                        pieces += 1 
                    else:
                        gaps.append([start_x, start_y])
                    start_x += 1
                    start_y += 1
                if start_x == stop:
                    if pieces == 2:
                        twos += 1 
                    if pieces == 3:
                        if (gaps[0][1] == 0 and board.get_item_value(gaps[0][0], gaps[0][1]) is None) or\
                              (gaps[0][1] > 0 and board.get_item_value(gaps[0][0], gaps[0][1]-1) is not None):
                            threes.append([row, True, gaps[0][0]])
                        else:
                            threes.append([row, False, gaps[0][0]])
                x, y = x+1, y+1
        if twos > 0 or len(threes) > 0:
            openings.append([row, {'twos': twos,'threes': threes}])
            
    return openings
                    