from pysc2.agents import base_agent
from pysc2.lib import actions

import logging

from Actions.sc2actions import SC2Action

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
    
    def step(self, obs):
        super(Agent, self).step(obs)
        act = SC2Action()
        return act.action()