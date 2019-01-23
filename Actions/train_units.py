from pysc2.lib import features, actions, units
from Actions.sc2actions import SC2Action
from Actions.lookup import LookUp
from UnitType.terran_units import Terran

# get help from
# https://chatbotslife.com/building-a-basic-pysc2-agent-b109cde1477c

class TrainUnits(SC2Action):

    # private fields
    _SUPPLY_USED = 3
    _SUPPLY_MAX = 4
    _RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id

    # public fields
    TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
    TRAIN_REAPER = actions.FUNCTIONS.Train_Reaper_quick.id
    TRAIN_MARAUDER = actions.FUNCTIONS.Train_Marauder_quick.id
    TRAIN_GHOST = actions.FUNCTIONS.Train_Ghost_quick.id

    def __init__(self, base_top_left, set_rally, to_train, number=5):
        super(TrainUnits, self).__init__(base_top_left)
        self._duration = 3
        self._set_rally = set_rally
        self._to_train = to_train
        self._itrain = 0
        self._number_of_train = number

    def _selectBarracks(self, obs):
        self._logger.debug("Selecting a barracks")
        y, x = (obs.observation["feature_screen"][self._UNIT_TYPE] == Terran.BARRACKS.value).nonzero()
        if(y.any()):
            target = (x.mean(), y.mean())
            result = actions.FUNCTIONS.select_point("select_all_type", target)
            self._logger.debug("Find one")
        else:
            self._iteration = self._duration + 1
            result = actions.FUNCTIONS.no_op()
            self._logger.debug("no barracks")
        return result

    def _setRallyPoint(self):
        self._logger.debug("Setting the rally point")
        result = actions.FunctionCall(self._RALLY_UNITS_MINIMAP, [self._NOT_QUEUED, [29, 46]])
        if self._base_top_left:
            result = actions.FunctionCall(self._RALLY_UNITS_MINIMAP, [self._NOT_QUEUED, [29, 21]])
        return result


    def _trainUnits(self):
        self._logger.debug("Training an unit")
        self._itrain += 1
        return actions.FunctionCall(self._to_train, [self._NOT_QUEUED])

    def action(self, obs):
        self._logger.debug("Performing action "+str(self._iteration))
        result = actions.FUNCTIONS.no_op()
        if self._iteration == 0:
            self._iteration += 1
            result = self._selectBarracks(obs)
        elif self._iteration == 1:
            if self._set_rally and self._RALLY_UNITS_MINIMAP in obs.observation["available_actions"]:result = self._setRallyPoint()
            self._iteration += 1
        elif self._iteration == 2  and self._to_train in obs.observation["available_actions"]:
            result = self._trainUnits()
            self._iteration += 1
        return result
        