from une_ai.models import Agent
from une_ai.models import GridMap

class ConnectFourPlayer(Agent):

    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)

    # TODO
    # add all the necessary sensors as per the requirements
    def add_all_sensors(self):
        self.add_sensor('game-board-sensor', GridMap(6,7, None), \
            lambda v: isinstance(v, GridMap) and all(\
            v.get_item_value(i,j) in ['Y', 'R', 'W', None] for i in v.get_width()\
                for j in v.get_height()))
        
        self.add_sensor('powerups-sensor', {'Y': None, 'R': None}, lambda v:\
            isinstance(v, dict) and len(v) == 2 and all(x in v.keys() and v[x] in\
            ['anvil', 'x2', 'wall', None] for x in ['Y', 'R']))
        
        self.add_sensor('turn-taking-indicator', 'Y', lambda v: v in ['Y', 'R'])

    # TODO
    # add all the necessary actuators as per the requirements
    def add_all_actuators(self):
        self.add_actuator('checker-handler', ('release', 0), lambda v: isinstance(v, tuple)\
            and len(v) == 2 and v[0] in ['release', 'popup'] and v[1] in range(7))
        
        self.add_actuator('powerup-selector', False, lambda v: isinstance(v, bool) and\
            v in [True, False])


    # TODO
    # add all the necessary actions as per the requirements
    def add_all_actions(self):
        for i in range(7):
            self.add_action('release-{0}'.format(i), lambda v: v.split('-')[0] == 'release'\
                and v.split('-')[1] in range(7))
        for i in range(7):
            self.add_action('popup-{0}'.format(i), lambda v: v.split('-')[0] == 'release'\
                and v.split('-')[1] in range(7))
        for i in range(7):
            self.add_action('use-power-up-{0}'.format(i), lambda v: v.split('-')[0] == 'release'\
                and v.split('-')[1] in range(7))
        