from pysc2.lib import features, actions, units
from Actions.lookup import LookUp
from UnitType.terran_units import Terran

class MoveArmy(LookUp):

    _ATTACK_MINIMAP = actions.FUNCTIONS.Move_screen.id
    
    def __init__(self,base_top_left):
        super(MoveArmy, self).__init__(base_top_left)
        self._duration = 4

    def _moveCameraToArmy(self):
        result = self._moveCamera(24,24)
        if self._base_top_left:result = self._moveCamera(24,46)
        return result

    def _selectArmy(self, obs):
        y, x = (obs.observation["feature_screen"][self._UNIT_TYPE] == Terran.MARINE.value).nonzero()
        if y.any():
            target = (x[0].mean(), y[0].mean())
            result = actions.FUNCTIONS.select_point("select_all_type", target)
            self._logger.debug("find army")
        else:
            self._iteration = self._duration
            result = actions.FUNCTIONS.no_op()
            self._logger.debug("no army found")
        return result

    def _moveToEnnemi(self):
        x, y = self.focusAtBase(not self._base_top_left)
        return actions.FunctionCall(self._ATTACK_MINIMAP, [self._NOT_QUEUED, [x,y]])

    def action(self, obs):
        result = actions.FUNCTIONS.no_op()
        if self._iteration == 0:
            result = self._moveCameraToArmy()
            self._iteration += 1
        elif self._iteration == 1:
            self._iteration +=1
            result = self._selectArmy(obs)
        elif self._iteration == 2:
            self._moveToEnnemi()
            self._iteration += 1
        elif self._iteration == 3:
            print("here i am")
            x, y = self.focusAtBase(self._base_top_left)
            result = self._moveCamera(x,y)
            self._iteration += 1
        input()
        return result
