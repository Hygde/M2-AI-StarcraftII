from pysc2.lib import features
from pysc2.lib import actions
from Actions.sc2actions import SC2Action

class LookUp(SC2Action):

    _MOVE_CAMERA = actions.FUNCTIONS.move_camera.id

    def __init__(self, base_top_left):
        super(LookUp, self).__init__(base_top_left)
        self._duration = 10

    def _moveCamera(self, x, y):
        self._logger.debug(self._MOVE_CAMERA)
        return actions.FUNCTIONS.move_camera([x, y])

    def getPositionOfTheMainBase(self, obs):
        unit_type = obs.observation["feature_screen"][self._UNIT_TYPE]
        yx = (unit_type == self._TERRAN_COMMANDCENTER).nonzero()
        return (yx[1].mean(), yx[0].mean())

    def focusAtBase(self, base_top_left):
        x, y = 0, 0
        if self.base_top_left: x, y = 18, 24
        else: x, y = 40, 46
        return (x, y)

    def action(self, obs):
        if self._iteration < 9:
            x, y = 20 * int(self._iteration/3) + 12, 20 * (self._iteration % 3) + 12
            self._logger.debug("x = "+str(x)+" y = "+str(y))
        else:
            x, y = self.focusAtBase(self.base_top_left)
        self._iteration += 1
        return self._moveCamera(x,y)


        