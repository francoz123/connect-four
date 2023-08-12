import traceback
import random

from une_ai.assignments import ConnectFourGame
from une_ai.models import GraphNode
from connect_four_environment import ConnectFourEnvironment

# A simple agent program choosing actions randomly
def random_behaviour(percepts, actuators):
    try:
        game_state = {
            'game-board': percepts['game-board-sensor'],
            'power-up-Y': percepts['powerups-sensor']['Y'],
            'power-up-R': percepts['powerups-sensor']['R'],
            'player-turn': percepts['turn-taking-indicator']
        }
    except KeyError as e:
        game_state = {}
        print("You may have forgotten to add the necessary sensors:")
        traceback.print_exc()

    if not ConnectFourEnvironment.is_terminal(game_state):
        legal_moves = ConnectFourEnvironment.get_legal_actions(game_state)
        try:
            action = random.choice(legal_moves)
        except IndexError as e:
            print("You may have forgotten to implement the ConnectFourEnvironment methods, or you implemented them incorrectly:")
            traceback.print_exc()
            return []

        return [action]
    else:
        return []

# An agent program to allow a human player to play Connect Four
# see the assignment's requirements for a list of valid keys
# to interact with the game
def human_agent(percepts, actuators):
    action = ConnectFourGame.wait_for_user_input()
    return [action]

# TODO
# complete the agent program to implement an intelligent behaviour for
# the agent player
def intelligent_behaviour(percepts, actuator):
    game_state = {
        'game-board': percepts['game-board-sensor'],
        'power-up-Y': percepts['powerups-sensor']['Y'],
        'power-up-R': percepts['powerups-sensor']['R'],
        'player-turn': percepts['turn-taking-indicator']
    }
    max_depth = 4
    root = GraphNode(game_state, None, None, 0)
    player_turn = ConnectFourEnvironment.turn(game_state)
    if not ConnectFourEnvironment.is_terminal(game_state):
        state_node = GraphNode(game_state, None, None, 0)
        #tic = time.time()
        _, best_move = minimax_alpha_beta(state_node, player_turn, float("-Inf"), float("+Inf"), max_depth)
        #toc = time.time()
        #print("[Minimax Alpha-Beta (player {0})] Elapsed (sec): {1:.6f}".format(player_turn, toc-tic))
        if best_move is not None:
            return [best_move]
    print('Best move ',best_move)
    return []

def minimax_alpha_beta(node, player, alpha, beta, depth):
    game_state = node.get_state()
    move_best = None
    legal_actions = ConnectFourEnvironment.get_legal_actions(game_state)

    player_turn = game_state['player-turn']
    is_maximising = player_turn == player

    if is_maximising:
        value = float('-Inf')
    else:
        value = float('+Inf')
    if depth <= 0 or ConnectFourEnvironment.is_terminal(game_state):
        value = ConnectFourEnvironment.payoff(game_state, player)
        return value, move_best
    
    for action in legal_actions:
        new_state = ConnectFourEnvironment.transition_result(game_state, action)
        child_node = GraphNode(new_state, node, action, 1)
        value_new, _ = minimax_alpha_beta(child_node, player, alpha, beta, depth - 1)
        if is_maximising:
            if value_new > value:
                value = value_new
                move_best = action
            alpha = max(value, alpha)
            if value >= beta:
                break
        else:
            if value_new < value:
                value = value_new
                move_best = action
            beta = min(value, beta)
            if value <= alpha:
                break
        
    return value, move_best

def optimised_minimax(node, player, tt, depth):
    game_state = node.get_state()
    player_turn = game_state['player-turn']
    is_maximising = player_turn == player

    # using transposition table
    tt_entry = tt.lookup(node)
    if tt_entry is not None and tt_entry['depth'] >= depth:
        return tt_entry['value'], tt_entry["move_best"]
    
    move_best = None
    
    if is_maximising:
        value = float('-Inf')
    else:
        value = float('+Inf')
    if depth <= 0 or ConnectFourEnvironment.is_terminal(game_state):
        value = ConnectFourEnvironment.payoff(game_state, player)
        return value, move_best
    
    legal_actions = ConnectFourEnvironment.get_legal_actions(game_state)
    for action in legal_actions:
        new_state = ConnectFourEnvironment.transition_result(game_state, action)
        child_node = GraphNode(new_state, node, action, 1)
        value_new, _ = optimised_minimax(child_node, player, tt, depth - 1)
        
        if (is_maximising and value_new > value) or (not is_maximising and value_new < value):
            value = value_new
            move_best = action

    # storing value in transposition table
    if tt_entry is None or tt_entry['depth'] <= depth:
        entry_dict = {
            "value": int(value),
            "depth": depth,
            "move_best": move_best
        }

        tt.store_node(node, entry_dict)

    return value, move_best