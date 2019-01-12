from pysc2.lib import features
from pysc2.lib import actions
from Actions.sc2actions import SC2Action

class LookUp(SC2Action):

    _MOVE_CAMERA = actions.FUNCTIONS.move_camera.id

    def __init__(self, base_top_left):
        super(LookUp, self).__init__(base_top_left)

    def getPositionOfTheMainBase(self, obs):
        unit_type = obs.observation["feature_screen"][self._UNIT_TYPE]
        yx = (unit_type == self._TERRAN_COMMANDCENTER).nonzero()
        return (yx[1].mean(), yx[0].mean())

    def moveCamera(self, x, y):
        self.logger.debug(self._MOVE_CAMERA)
        return actions.FUNCTIONS.move_camera([x, y])