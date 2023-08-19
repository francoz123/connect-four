def horizontals(board, player):
    opponent_colour = 1 if player == 2 else 2
    openings = []
    print('player', player)
    # Calculate horizontal twos
    for row in range(len(board)):
        twos, threes = 0, []
        for col in range(len(board[0])-3):
            start, stop, gaps = col, col + 3, []
            pieces = 0
            #print('New row: ', row, col)
            while start <= stop and board[row][start] != opponent_colour:
                #print('item', board[row][start])
                if board[row][start] == player:
                    print('player', player)
                    pieces += 1 
                else:
                    gaps.append(start)
                start += 1
            print('pieces', pieces)
            if start == stop + 1:
                if pieces == 2:
                    twos += 1 
                if pieces == 3:
                    if (row == 5  and board[row][gaps[0]] == 0) or (row < 5 and board[row-1][gaps[0]] == 0):
                        threes.append([row, True, gaps[0]])
                    else:
                        threes.append([row, False, gaps[0]])
            print('twos', twos)
        if twos > 0 or len(threes) > 0:
            openings.append([row, {'twos': twos,'threes': threes}])
    return openings

def right_diagonals(board, player):
    opponent_colour = 1 if player == 2 else 2
    openings = []
    end = 3
    number = 3
    # Calculate horizontal twos
    for col in range(end + 1):
        for row in (range(1) if col > 0 else range(3)):
            twos, threes = 0, []
            x, y,  = col, row
            col_end = 5-y if x < 1 else 6
            row_end = 5 if x <= 1 else 6-x
            stop_col = col_end-3
            stop_row = 2 if x <= 1 else 1 if x == 2 else 0
            #print('st', col, row, 'end', col_end, row_end, 'stp', stop_col, stop_row)
            while x <= stop_col and y <= stop_row:
                pieces = 0
                start_x, start_y, stop, gaps = x, y, x + 3, []
                while start_x <= stop and board[start_y][start_x] != opponent_colour:
                    print('st', start_x, start_y)
                    if board[start_y][start_x] == player:
                        #print('player', player)
                        pieces += 1 
                    else:
                        gaps.append([start_y, start_x])
                    start_x += 1
                    start_y += 1
                if start_x == stop + 1:
                    if pieces == 2:
                        #print('pieces', pieces)
                        twos += 1 
                    if pieces == 3:
                        if (gaps[0][0] == 0 and board[gaps[0][0]][gaps[0][1]] == 0) or\
                              (gaps[0][0] < 5 and board[gaps[0][0]+1][gaps[0][1]] != 0):
                            threes.append([row, True, gaps[0][0]])
                        else:
                            threes.append([row, False, gaps[0][1]])
                x, y = x+1, y+1
            if twos > 0 or len(threes) > 0:
                openings.append([number, {'twos': twos,'threes': threes}])
            number += 1
        

    return openings
    
def left_diagonals(board, player):
    opponent_colour = 1 if player == 2 else 2
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
                print('new')
                while start_x <= stop and board[start_y][start_x] != opponent_colour:
                    print('st', start_x, start_y)
                    if board[start_y][start_x] == player:
                        pieces += 1 
                    else:
                        gaps.append([start_y, start_x])
                    start_x += 1
                    start_y -= 1
                if start_x == stop + 1:
                    if pieces == 2:
                        twos += 1 
                    if pieces == 3:
                        if (gaps[0][0] == 5 and board[gaps[0][0]][gaps[0][1]] == 0) or\
                              (gaps[0][0] < 5 and board[gaps[0][0]+1][gaps[0][1]] != 0):
                            threes.append([row, True, gaps[0][0]])
                        else:
                            threes.append([row, False, gaps[0][1]])
                x, y = x+1, y-1
            if twos > 0 or len(threes) > 0:
                openings.append([number, {'twos': twos,'threes': threes}])
            number += 1
        

    return openings