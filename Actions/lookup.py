from pysc2.lib import features
from pysc2.lib import actions
from Actions.sc2actions import SC2Action

class LookUp(SC2Action):

    _MOVE_CAMERA = actions.FUNCTIONS.move_camera.id

    def __init__(self, base_top_left):
        super(LookUp, self).__init__(base_top_left)
        self.duration = 10

    def getPositionOfTheMainBase(self, obs):
        unit_type = obs.observation["feature_screen"][self._UNIT_TYPE]
        yx = (unit_type == self._TERRAN_COMMANDCENTER).nonzero()
        return (yx[1].mean(), yx[0].mean())

    def moveCamera(self, x, y):
        self.logger.debug(self._MOVE_CAMERA)
        return actions.FUNCTIONS.move_camera([x, y])

    def action(self, obs):
        if self.iteration < 9:
            x, y = 20 * int(self.iteration/3) + 12, 20 * (self.iteration % 3) + 12
            self.logger.debug("x = "+str(x)+" y = "+str(y))
        else:
            if self.base_top_left: x, y = 18, 24
            else: x, y = 40, 46
        self.iteration += 1
        return self.moveCamera(x,y)


        