from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import logging

from Actions.sc2actions import SC2Action
from Actions.builder import Builder

#python -m pysc2.bin.agent --agent agent.Agent --map Simple64 --agent_race terran

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
        self.iteration = 0

    def getBasePosition(self, obs):
        if (self.iteration == 0) :
            player_pos = (obs.observation["feature_minimap"][features.SCREEN_FEATURES.player_relative.index] == 1).nonzero()
            self.base_top_left = player_pos[0].mean() <= 31
            self.logger.debug("The main base is on the "+ ("top left" if self.base_top_left else "bottom right") + " corner")

    def init(self, obs):
        self.getBasePosition(obs)
    
    def step(self, obs):
        super(Agent, self).step(obs)
        if self.iteration == 0:self.init(obs)
        act = SC2Action(self.base_top_left)
        self.iteration += 1
        return act.action(obs)