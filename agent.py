from pysc2.agents import base_agent
from pysc2.lib import actions, features

import logging

from Actions.sc2actions import SC2Action
from Actions.builder import Builder
from Actions.lookup import LookUp

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
        self._logger.addHandler(ch)
        self._act = None

    def reset(self):
        super(Agent, self).reset()
        self.steps = 0

    def getBasePosition(self, obs):
        player_pos = (obs.observation["feature_minimap"][features.SCREEN_FEATURES.player_relative.index] == 1).nonzero()
        self.base_top_left = player_pos[0].mean() <= 31
        self._logger.debug("The main base is on the "+ ("top left" if self.base_top_left else "bottom right") + " corner")
        self.built = False

    def init(self, obs):
        self.getBasePosition(obs)
        self.base_position = LookUp(self.base_top_left).getPositionOfTheMainBase(obs)
        self._logger.debug(self.base_position)
        self.buildings = {Builder.BUILD_SUPPLYDEPOT:0, Builder.BUILD_BARRACKS:0, Builder.BUILD_ENGINEERINGBAY:0, Builder.BUILD_BUNKER:0, Builder.BUILD_AUTOTURRET:0}
        self._act = Builder(self.base_top_left, self.buildings, Builder.BUILD_SUPPLYDEPOT)
    
    def step(self, obs):
        super(Agent, self).step(obs)
        self._logger.debug("steps = "+str(self.steps))
        result = actions.FUNCTIONS.no_op()
        if self.steps == 1:
            self.init(obs)
            #self._act = LookUp(self.base_top_left)
        elif not self._act.isFinished():
            result = self._act.action(obs)
        else:
            self.buildings[Builder.BUILD_SUPPLYDEPOT] += 1
            if not self.built:
                self._act = Builder(self.base_top_left, self.buildings, Builder.BUILD_BARRACKS)
                self.built = True

        return result