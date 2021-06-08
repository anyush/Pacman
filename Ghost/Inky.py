from Ghost.Ghost import *
from Directions import Directions
from config import INKY_START_POSITION, INKY_SCATTER_TARGET, INKY_POINTS_EATEN_START


class Inky(Ghost):
    def __init__(self, pacman, blinky):
        super().__init__(Colors.cyan, Directions.right, GhostStates.waiting, INKY_START_POSITION,
                         pacman, INKY_SCATTER_TARGET)
        self.blinky = blinky

    def reset(self):
        self.position = list(INKY_START_POSITION)
        self.direction = Directions.right
        self.state = GhostStates.waiting
        super().reset()

    def find_direction(self, field_real, *args):
        super().find_direction(field_real, (2 * self.pacman.position[0] - self.blinky.position[1],
                                            2 * self.pacman.position[0] - self.blinky.position[1]))

    def update_state(self, timer, dots_eaten):
        if self.state is GhostStates.waiting and dots_eaten > INKY_POINTS_EATEN_START:
            self.state = GhostStates.scatter
        if self.state is not GhostStates.waiting:
            super().update_state(timer, dots_eaten)
