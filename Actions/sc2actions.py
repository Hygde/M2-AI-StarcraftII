from pysc2.agents import base_agent
from pysc2.lib import features
from pysc2.lib import actions

import logging

class SC2Action:

    #functions
    _NOOP = actions.FUNCTIONS.no_op.id
    _SELECT_POINT = actions.FUNCTIONS.select_point.id
    
    #features
    _PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
    _UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

    #terrans unit id
    _TERRAN_COMMANDCENTER = 18
    _TERRAN_SCV = 45

    #params
    _SELF = 1
    _NOT_QUEUED = [0]
    _QUEUED = [1]

    def __init__(self):
        self.logger = logging.getLogger()

    def action(self):
        self.logger.debug("Performing action")
        return actions.FunctionCall(self._NOOP, [])
    