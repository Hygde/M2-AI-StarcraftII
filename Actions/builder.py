from Actions.sc2actions import SC2Action

from pysc2.lib import features, actions, units

class Builder(SC2Action):

    _PLAYER_NEUTRAL = features.PlayerRelative.NEUTRAL

    #terrans unit id
    _TERRAN_COMMANDCENTER = 18
    _TERRAN_SCV = 45

    _BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
    _BUILD_BARRAQUEMENT = actions.FUNCTIONS.Build_Barracks_screen.id

    def __init__(self, base_top_left):
        super(Builder,self).__init__(base_top_left)
        self.duration = 3

    def _selectSCV(self, obs):
        self.logger.debug("Selecting a SCV")
        yx = (obs.observation["feature_screen"][self._UNIT_TYPE] == self._TERRAN_SCV).nonzero()
        target = [yx[1][0], yx[0][0]]
        return actions.FunctionCall(self._SELECT_POINT, [self._NOT_QUEUED, target])

    def _buildSupplyDepot(self, obs):#todo generalize this function
        self.logger.debug("")
        unit_type = obs.observation["feature_screen"][self._UNIT_TYPE]
        yx = (unit_type == self._TERRAN_COMMANDCENTER).nonzero()
        target = self._transformLocation(int(yx[1].mean()), 0, int(yx[0].mean()), 20)
        return actions.FunctionCall(self._BUILD_SUPPLYDEPOT, [self._NOT_QUEUED, target])

    def _freeSCV(self, obs):
        self.logger.debug("Freeing the SCV")
        yx_min = (obs.observation["feature_screen"][self._UNIT_TYPE] == self.NEUTRAL_MINERALFIELD).nonzero()
        self.logger.debug(yx_min);input()
        target = self._transformLocation(int(yx_min[1].mean()), 0, int(yx_min[0].mean()), 0)
        return actions.FunctionCall(self._MOVE_TO, [self._QUEUED, target])

    def action(self, obs):
        if self.iteration == 0:
            result = self._selectSCV(obs)
            self.iteration += 1
        elif self._BUILD_SUPPLYDEPOT in obs.observation["available_actions"] and self.iteration < 2:
            result = self._buildSupplyDepot(obs)
            self.iteration +=1
        elif self.iteration == 2:
            self.iteration += 1
            result = self._freeSCV(obs)
        else:result = actions.FUNCTIONS.no_op()
        return result
