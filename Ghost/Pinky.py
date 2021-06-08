from Ghost.Ghost import *
from Directions import Directions
from config import PINKY_START_POSITION, PINKY_SCATTER_TARGET


class Pinky(Ghost):
    def __init__(self, pacman):
        super().__init__(Colors.magenta, Directions.up, GhostStates.scatter, PINKY_START_POSITION,
                         pacman, PINKY_SCATTER_TARGET)

    def reset(self):
        self.position = list(PINKY_START_POSITION)
        self.direction = Directions.up
        self.state = GhostStates.scatter
        super().reset()

    def find_direction(self, field_real, *args):
        targets = {Directions.up: (self.pacman.position[0], self.pacman.position[1] - 3),
                   Directions.down: (self.pacman.position[0], self.pacman.position[1] + 3),
                   Directions.left: (self.pacman.position[0] - 3, self.pacman.position[1]),
                   Directions.right: (self.pacman.position[0] + 3, self.pacman.position[1])
                   }

        super().find_direction(field_real, targets[self.pacman.direction])
