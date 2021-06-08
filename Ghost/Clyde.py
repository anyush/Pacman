from Ghost.Ghost import *
from Directions import Directions
from math import sqrt
from config import CLYDE_START_POSITION, CLYDE_SCATTER_TARGET, CLYDE_POINTS_EATEN_START


class Clyde(Ghost):
    def __init__(self, pacman):
        super().__init__(Colors.green, Directions.left, GhostStates.waiting, CLYDE_START_POSITION,
                         pacman, CLYDE_SCATTER_TARGET)

    def reset(self):
        self.position = list(CLYDE_START_POSITION)
        self.direction = Directions.left
        self.state = GhostStates.waiting
        super().reset()

    def find_direction(self, field_real, *args):
        dist = sqrt((self.pacman.position[0] - self.position[0]) ** 2 +
                    (self.pacman.position[1] - self.position[1]) ** 2)
        if dist > 8:
            chase_target = self.pacman.position
        else:
            chase_target = CLYDE_SCATTER_TARGET

        super().find_direction(field_real, chase_target)

    def update_state(self, timer, dots_eaten):
        if self.state is GhostStates.waiting and dots_eaten > CLYDE_POINTS_EATEN_START:
            self.state = GhostStates.scatter
        if self.state is not GhostStates.waiting:
            super().update_state(timer, dots_eaten)
