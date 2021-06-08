from Ghost.Ghost import *
from config import BLINKY_START_POSITION, BLINKY_SCATTER_TARGET


class Blinky(Ghost):
    def __init__(self, pacman):
        super().__init__(Colors.red, Directions.right, GhostStates.scatter, BLINKY_START_POSITION,
                         pacman, BLINKY_SCATTER_TARGET)

    def find_direction(self, field_real, *args):
        super().find_direction(field_real, tuple(self.pacman.position))

    def reset(self):
        self.position = list(BLINKY_START_POSITION)
        self.direction = Directions.right
        self.state = GhostStates.scatter
        super().reset()
