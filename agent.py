from pysc2.agents import base_agent
from pysc2.lib import actions, features

import logging

from Actions.sc2actions import SC2Action
from Actions.builder import Builder

# List of known unit types. It is taken from:
# https://github.com/Blizzard/s2client-api/blob/master/include/sc2api/sc2_typeenums.h

# How to run:
# python -m pysc2.bin.agent --agent agent.Agent --map Simple64 --agent_race terran

class Agent(base_agent.BaseAgent):
    def __init__(self):
        super(Agent, self).__init__()
        self.logger = logging.getLogger()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s :: %(message)s")
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.act = None

    def getBasePosition(self, obs):
        player_pos = (obs.observation["feature_minimap"][features.SCREEN_FEATURES.player_relative.index] == 1).nonzero()
        self.base_top_left = player_pos[0].mean() <= 31
        self.logger.debug("The main base is on the "+ ("top left" if self.base_top_left else "bottom right") + " corner")

    def init(self, obs):
        self.getBasePosition(obs)
    
    def step(self, obs):
        super(Agent, self).step(obs)
        self.logger.debug("steps = "+str(self.steps))
        self.logger.debug(actions.FUNCTIONS_AVAILABLE)
        result = actions.FUNCTIONS.no_op()
        if self.steps == 1:
            self.init(obs)
            self.act = Builder(self.base_top_left)
        elif not self.act.isFinished():
            result = self.act.action(obs)

        return  result