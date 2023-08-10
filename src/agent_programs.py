import traceback
import random

from une_ai.assignments import ConnectFourGame
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
    return []

