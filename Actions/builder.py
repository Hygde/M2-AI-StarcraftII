from Actions.sc2actions import SC2Action

from pysc2.lib import features, actions, units

class Builder(SC2Action):
    #private fields
    _PLAYER_NEUTRAL = features.PlayerRelative.NEUTRAL
    _TERRAN_SCV = 45#terrans unit id

    #public fields
    BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
    BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
    BUILD_ENGINEERINGBAY = actions.FUNCTIONS.Build_EngineeringBay_screen.id
    BUILD_AUTOTURRET = actions.FUNCTIONS.Build_MissileTurret_screen.id
    BUILD_BUNKER = actions.FUNCTIONS.Build_Bunker_screen.id

    def __init__(self, base_top_left, buildings, to_build=BUILD_SUPPLYDEPOT):
        super(Builder,self).__init__(base_top_left)
        self._duration = 4
        self._to_build = to_build
        self._buildings = buildings

    def _selectSCV(self, obs):
        self._logger.debug("Selecting a SCV")
        yx = (obs.observation["feature_screen"][self._UNIT_TYPE] == self._TERRAN_SCV).nonzero()
        target = [yx[1][0], yx[0][0]]
        return actions.FunctionCall(self._SELECT_POINT, [self._QUEUED, target])

    def _offsetByBuildingType(self, btype):
        if   btype == self.BUILD_SUPPLYDEPOT:      x, y = 0 * self._buildings[btype]    , 5 * self._buildings[btype] + 15
        elif btype == self.BUILD_BARRACKS:         x, y = 5 * self._buildings[btype] + 15, 5 * self._buildings[btype] + 15
        elif btype == self.BUILD_ENGINEERINGBAY:   x, y = 5 * self._buildings[btype] + 15, 0 * self._buildings[btype]
        return (x, y)

    def _build(self, obs):#todo generalize this function
        self._logger.debug("")
        unit_type = obs.observation["feature_screen"][self._UNIT_TYPE]
        yx = (unit_type == self._TERRAN_COMMANDCENTER).nonzero()
        xy_off = self._offsetByBuildingType(self._to_build)
        self._logger.debug(xy_off); input()
        target = self._transformLocation(int(yx[1].mean()), xy_off[0], int(yx[0].mean()), xy_off[1])
        return actions.FunctionCall(self._to_build, [self._QUEUED, target])

    def _extractMineral(self, obs):
        self._logger.debug("Freeing the SCV")
        yx_min = (obs.observation["feature_screen"][self._UNIT_TYPE] == self.NEUTRAL_MINERALFIELD).nonzero()
        target = self._transformLocation(int(yx_min[1].mean()), 0, int(yx_min[0].mean()), 0)
        return actions.FunctionCall(self._MOVE_TO, [self._QUEUED, target])

    def action(self, obs):
        if self._iteration == 0:
            result = self._selectSCV(obs)
            self._iteration += 1
        elif self._to_build in obs.observation["available_actions"] and self._iteration < 2:
            result = self._build(obs)
            self._iteration +=1
        elif self._iteration == 2:
            self._iteration += 1
            result = self._extractMineral(obs)
        elif self._iteration == 3:
            result = self._selectSCV(obs)
            self._iteration += 1
        else:result = actions.FUNCTIONS.no_op()
        return result
