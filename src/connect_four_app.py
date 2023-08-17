from une_ai.assignments import ConnectFourGame
from connect_four_environment import ConnectFourEnvironment
from connect_four_player import ConnectFourPlayer
from agent_programs import random_behaviour, human_agent, intelligent_behaviour, agent_program_mcts, agent_program_optimised_minimax,\
agent_program_optimised_minimax_ab
from connectfour_ttable import ConnectFourTTable

if __name__ == '__main__':
    # Creating the transposition table
    tt = ConnectFourTTable(instance_id='b61e431c-3a88-11ee-8af2-001636443811')
    print("Initialised a Transposition table with instance id {0}".format(tt.get_instance_id()))

    wrapped_minimax_tt = lambda perc, act: agent_program_optimised_minimax(perc, act, tt, max_depth=5)
    wrapped_minimax_ab_tt = lambda perc, act: agent_program_optimised_minimax_ab(perc, act, tt, max_depth=7)
    # Change these two lines to instantiate players with proper
    # agent programs, as per your tests
    wrapped_mcts = lambda p, a:  agent_program_mcts(p, a, max_time = 20)
    wrapped_inteligent_behaviour = lambda p, a: intelligent_behaviour(p, a, max_depth=4)
    yellow_player = ConnectFourPlayer('Y', wrapped_inteligent_behaviour)
    red_player = ConnectFourPlayer('R', wrapped_inteligent_behaviour)

    # DO NOT EDIT THESE LINES OF CODE!!!
    game_environment = ConnectFourEnvironment()
    game_environment.add_player(yellow_player)
    game_environment.add_player(red_player)

    game = ConnectFourGame(yellow_player, red_player, game_environment)