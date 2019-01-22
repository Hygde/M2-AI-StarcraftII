from Actions.sc2actions import SC2Action

from pysc2.lib import features, actions, units

from Actions.lookup import LookUp
from UnitType.terran_units import Terran

class Builder(SC2Action):
    #private fields
    _PLAYER_NEUTRAL = features.PlayerRelative.NEUTRAL

    #public fields
    BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
    BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
    BUILD_ENGINEERINGBAY = actions.FUNCTIONS.Build_EngineeringBay_screen.id
    BUILD_AUTOTURRET = actions.FUNCTIONS.Build_MissileTurret_screen.id
    BUILD_BUNKER = actions.FUNCTIONS.Build_Bunker_screen.id

    def __init__(self, base_top_left, buildings, number_of_building, to_build=BUILD_SUPPLYDEPOT):
        super(Builder,self).__init__(base_top_left)
        self._duration = 3
        self._to_build = to_build
        self._buildings = buildings
        self._number_building = number_of_building

    def _selectSCV(self, obs):
        self._logger.debug("Selecting a SCV")
        yx = (obs.observation["feature_screen"][self._UNIT_TYPE] == Terran.SCV.value).nonzero()
        target = [yx[1][0], yx[0][0]]
        return actions.FunctionCall(self._SELECT_POINT, [self._NOT_QUEUED, target])

    def _offsetByBuildingType(self, btype):
        if self._number_building == 0: x, y = 00 ,12
        if self._number_building == 1: x, y = 12 ,12
        if self._number_building == 2: x, y = 22 ,12
        if self._number_building == 3: x, y = 00 ,22
        if self._number_building == 4: x, y = 12 ,22
        if self._number_building == 5: x, y = 22 ,22
        return (x, y)

    def _checkState(self, obs):
        result = False
        count = LookUp(self._base_top_left).countUnit(obs, self.buildFuncToUnit(self._to_build))
        if count >= self._buildings[self._to_build]+1:result = True
        return result

    def _build(self, obs):#todo generalize this function
        self._logger.debug("")
        unit_type = obs.observation["feature_screen"][self._UNIT_TYPE]
        yx = (unit_type == self._TERRAN_COMMANDCENTER).nonzero()
        xy_off = self._offsetByBuildingType(self._to_build)
        target = self._transformLocation(int(yx[1].mean()), xy_off[0], int(yx[0].mean()), xy_off[1])
        return actions.FunctionCall(self._to_build, [self._QUEUED, target])

    def _extractMineral(self, obs):
        self._logger.debug("Freeing the SCV")
        yx_min = (obs.observation["feature_screen"][self._UNIT_TYPE] == self.NEUTRAL_MINERALFIELD).nonzero()
        target = self._transformLocation(int(yx_min[1].mean()), 0, int(yx_min[0].mean()), 0)
        return actions.FunctionCall(self._MOVE_TO, [self._QUEUED, target])

    def buildFuncToUnit(self, func):
        result = Terran.SUPPLYDEPOT.value
        if(func == self.BUILD_BARRACKS):result = Terran.BARRACKS.value
        elif(func == self.BUILD_ENGINEERINGBAY):result = Terran.ENGINEERINGBAY.value
        return result

    def action(self, obs):
        result = actions.FUNCTIONS.no_op()
        if self._iteration == 0:
            result = self._selectSCV(obs)
            self._iteration += 1
        elif self._to_build in obs.observation["available_actions"] and self._iteration < 2:
            result = self._build(obs)
            self._iteration +=1
        elif self._iteration == 2:
            self._iteration += 1
            result = self._extractMineral(obs)
        return result
