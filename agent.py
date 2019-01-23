from math import pow
from pysc2.agents import base_agent
from pysc2.lib import actions, features

import logging

from Actions.sc2actions import SC2Action
from Actions.builder import Builder
from Actions.lookup import LookUp
from Actions.train_units import TrainUnits
from UnitType.terran_units import Terran
from Learning.qlearning import QTable

# List of known unit types. It is taken from:
# https://github.com/Blizzard/s2client-api/blob/master/include/sc2api/sc2_typeenums.h

# How to run:
# python -m pysc2.bin.agent --agent agent.Agent --map Simple64 --agent_race terran

class Agent(base_agent.BaseAgent):
    def __init__(self):
        super(Agent, self).__init__()
        self._logger = logging.getLogger()
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s :: %(message)s")
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self._building_reward = 0
        self._logger.addHandler(ch)
        self._act = None
        self._iteration = 0

    def reset(self):
        super(Agent, self).reset()
        self.steps = 0
        self._reward = 0

    def getBasePosition(self, obs):
        player_pos = (obs.observation["feature_minimap"][features.SCREEN_FEATURES.player_relative.index] == 1).nonzero()
        self.base_top_left = player_pos[0].mean() <= 31
        self._logger.debug("The main base is on the "+ ("top left" if self.base_top_left else "bottom right") + " corner")
        self.built = False

    def _init(self, obs):
        self.getBasePosition(obs)
        self.base_position = LookUp(self.base_top_left).getPositionOfTheMainBase(obs)
        self._logger.debug(self.base_position)
        self.buildings_state = {Builder.BUILD_SUPPLYDEPOT:0, Builder.BUILD_BARRACKS:0, Builder.BUILD_ENGINEERINGBAY:0}
        self._act = Builder(self.base_top_left, self.buildings_state, self._countBuildings(self._getBuildingState()))
        #self._qbuildings = QTable({Builder.BUILD_SUPPLYDEPOT:2, Builder.BUILD_BARRACKS:2, Builder.BUILD_ENGINEERINGBAY:1}, [Builder.BUILD_SUPPLYDEPOT, Builder.BUILD_BARRACKS, Builder.BUILD_ENGINEERINGBAY])
        self._qbuildings = QTable([Builder.BUILD_SUPPLYDEPOT, Builder.BUILD_BARRACKS, Builder.BUILD_ENGINEERINGBAY])
    
    def _getBuildingState(self):
        return (self.buildings_state[Builder.BUILD_SUPPLYDEPOT], self.buildings_state[Builder.BUILD_BARRACKS], self.buildings_state[Builder.BUILD_ENGINEERINGBAY])

    def _getReward(self, n):
        return 1 * pow(0.9,n)

    def _countBuildings(self, state):
        result = 0
        for el in state:result += el
        return result
    
    def step(self, obs):
        super(Agent, self).step(obs)
        self._logger.debug("epsiodes = "+str(self.episodes)+" steps = "+str(self.steps))
        result = actions.FUNCTIONS.no_op()

        if self.steps == 1:self._init(obs)
        elif not self._act.isFinished():result = self._act.action(obs)
        else:
            bstate = self._getBuildingState()
            for i, el in enumerate(self.buildings_state):self.buildings_state[el] = bstate[i]
            if self._countBuildings(bstate) < 5:#less than 5 buildings
                selected_action = self._qbuildings.get_action(bstate)
                next_state = list(bstate)
                next_state[selected_action] += 1
                next_act = [key for key in self.buildings_state][selected_action]
                self.buildings_state[next_act] += 1
                self._building_reward = self._qbuildings.update_qtable(bstate, tuple(next_state), selected_action, self._getReward(self.buildings_state[next_act]))#update reward
                self._act = Builder(self.base_top_left, self.buildings_state, self._countBuildings(next_state), next_act)
            elif self.steps > 300:
                if self._iteration < 10:
                    self._act = TrainUnits(self.base_top_left, True, TrainUnits.TRAIN_MARINE)
                    self._iteration += 1
                else:
                    self._iteration = 0

        return result