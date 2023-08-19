import traceback
import random
import time

from une_ai.models import GraphNode, MCTSGraphNode
from une_ai.assignments import ConnectFourGame
from connect_four_environment import ConnectFourEnvironment
from MCTS_functions import mcts
from minimax_functions import minimax, minimax_alpha_beta, optimised_minimax, optimised_minimax_alpha_beta

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
def intelligent_behaviour(percepts, actuator, max_depth = 4):
    player_turn = percepts['turn-taking-indicator']
    other = 'Y' if player_turn == 'R' else 'R'
    game_state = {
        'game-board': percepts['game-board-sensor'],
        'power-up-Y': percepts['powerups-sensor']['Y'],
        'power-up-R': percepts['powerups-sensor']['R'],
        'player-turn': player_turn
    }
    root = GraphNode(game_state, None, None, 0)
    player_turn = ConnectFourEnvironment.turn(game_state)
    if not ConnectFourEnvironment.is_terminal(game_state):
        state_node = GraphNode(game_state, None, None, 0)
        tic = time.time()
        _, best_move = minimax_alpha_beta(state_node, player_turn, float("-Inf"), float("+Inf"), max_depth)
        toc = time.time()
        print("[Minimax Alpha-Beta (player {0})] Elapsed (sec): {1:.6f}".format(player_turn, toc-tic))
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

def agent_program_optimised_minimax(percepts, actuators, tt, max_depth=4):
    player = percepts['turn-taking-indicator']
    game_state = {
        'game-board': percepts['game-board-sensor'],
        'power-up-Y': percepts['powerups-sensor']['Y'],
        'power-up-R': percepts['powerups-sensor']['R'],
        'player-turn': player
    }

    
    if not ConnectFourEnvironment.is_terminal(game_state):
        state_node = GraphNode(game_state, None, None, 0)
        tic = time.time()
        _, best_move = optimised_minimax(state_node, player, tt, max_depth)
        toc = time.time()
        print("[Optimised Minimax (player {0})] Elapsed (sec): {1:.6f}".format(player, toc-tic))
        if best_move is not None:
            return [best_move]
    
    return []

def agent_program_optimised_minimax_ab(percepts, actuators, tt, max_depth=4):
    player = percepts['turn-taking-indicator']
    game_state = {
        'game-board': percepts['game-board-sensor'],
        'power-up-Y': percepts['powerups-sensor']['Y'],
        'power-up-R': percepts['powerups-sensor']['R'],
        'player-turn': player
    }

    
    if not ConnectFourEnvironment.is_terminal(game_state):
        state_node = GraphNode(game_state, None, None, 0)
        tic = time.time()
        _, best_move = optimised_minimax_alpha_beta(state_node, player, float("-Inf"), float("+Inf"),tt, max_depth)
        toc = time.time()
        print("[Optimised Minimax (player {0})] Elapsed (sec): {1:.6f}".format(player, toc-tic))
        if best_move is not None:
            return [best_move]
    
    return []

def agent_program_mcts(percepts, actuators, max_time=1):
    player = percepts['turn-taking-indicator']
    game_state = {
        'game-board': percepts['game-board-sensor'],
        'power-up-Y': percepts['powerups-sensor']['Y'],
        'power-up-R': percepts['powerups-sensor']['R'],
        'player-turn': player
    }
    
    if not ConnectFourEnvironment.is_terminal(game_state):
        tic = time.time()
        root_node = MCTSGraphNode(game_state, None, None)
        best_move = mcts(root_node, player, max_time)
        toc = time.time()
        print("[MTCS (player {0})] Elapsed (sec): {1:.6f}".format(player, toc-tic))
        if best_move is not None:
            return [best_move]
    
    return []