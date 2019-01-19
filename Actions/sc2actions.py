from pysc2.lib import features
from pysc2.lib import actions

import logging

class SC2Action:

    NEUTRAL_MINERALFIELD = 341

    #terran main units
    _TERRAN_COMMANDCENTER = 18

    #functions
    _NOOP = actions.FUNCTIONS.no_op.id
    _SELECT_POINT = actions.FUNCTIONS.select_point.id
    _MOVE_TO = actions.FUNCTIONS.Move_screen.id
    
    #features
    _PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
    _UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
    _SELECTED = features.SCREEN_FEATURES.selected.index

    #params
    _SELF = 1
    _NOT_QUEUED = [0]
    _QUEUED = [1]

    def __init__(self, base_top_left):
        self._logger = logging.getLogger("SC2Action")
        self.base_top_left = base_top_left
        self._iteration = 0
        self._duration = 1

    def _transformLocation(self, x, x_distance, y, y_distance):
        self._logger.debug("calculating the position")
        if self.base_top_left:result = [x + x_distance, y + y_distance]
        else: result = [x - x_distance, y - y_distance]
        return result

    def action(self, obs):
        self._logger.debug("Performing action")
        return actions.FunctionCall(self._NOOP, [])

    def isFinished(self):
        result = self._iteration >= self._duration
        self._logger.debug(result)
        return result
    