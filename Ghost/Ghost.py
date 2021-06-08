from abc import ABC, abstractmethod
from enum import Enum
from Colors import Colors
from Directions import Directions
from Printer import Printer
from PointToScreenConverter import PointToScreenConverter as PTSConverter
from random import randint
from math import sqrt
from config import KILLED_TARGET, SCATTER_TIME, CHASE_TIME, FRIGHTENED_TIME, GHOST_0_FILENAME, GHOST_1_FILENAME


class GhostStates(Enum):
    waiting = 0
    scatter = 1
    chase = 2
    killed = 3
    frightened = 4


class Ghost(ABC):
    textures = []

    def __init__(self, color, direction, state, position, pacman, scatter_target):
        self.color = color
        self.move_n = 0
        self.anim = 0
        self.direction = direction
        self.state = state
        self.position = list(position)
        self.pacman = pacman
        self.scatter_target = scatter_target
        self.init_textures()
        self.last_frightened = -FRIGHTENED_TIME

        self.last_point = (3, 3)
        self.last_energetic = (3, 9)

    def reset(self):
        self.anim = 0

    def init_textures(self):
        tex_names = (GHOST_0_FILENAME, GHOST_1_FILENAME)
        for tex_name in tex_names:
            with open(tex_name, "r") as tex_file:
                texture = "".join(list(tex_file))
                self.textures.append(texture)

    def clear(self):
        texture = self.textures[self.anim]
        print(Colors.black.value)
        coords = PTSConverter.convert(self.position)
        for i, line in enumerate(texture.split("\n")):
            print(f"\033[{coords[1] + i};{coords[0] - 1}H" + line)

    def draw(self, color):
        texture = self.textures[self.anim]
        texture = texture.replace("#", color.value + "#")
        texture = texture.replace(" ", Colors.black.value + " ")
        texture = texture.replace("W", Colors.white.value + "#")
        coords = PTSConverter.convert(self.position)
        for i, line in enumerate(texture.split("\n")):
            print(f"\033[{coords[1] + i};{coords[0]-1}H" + line)

    @abstractmethod
    def find_direction(self, field_real, chase_coords):
        tile = field_real[self.position[1]][self.position[0]]
        if tile.can_turn == 0:
            return

        targets = {GhostStates.waiting: KILLED_TARGET,
                   GhostStates.scatter: self.scatter_target,
                   GhostStates.chase: chase_coords,
                   GhostStates.killed: KILLED_TARGET,
                   GhostStates.frightened: (randint(0, 81), randint(0, 93))
                   }

        allowed_moves = {Directions.up: False,
                         Directions.down: False,
                         Directions.left: False,
                         Directions.right: False
                         }

        positions_to_check = {Directions.up: (self.position[0], self.position[1]-3),
                              Directions.down: (self.position[0], self.position[1]+3),
                              Directions.left: (self.position[0]-3, self.position[1]),
                              Directions.right: (self.position[0]+3, self.position[1])
                              }

        cant_choose_direction = {Directions.up: Directions.down,
                                 Directions.down: Directions.up,
                                 Directions.left: Directions.right,
                                 Directions.right: Directions.left
                                 }

        target = targets[self.state]

        for direction in list(Directions):
            pos = positions_to_check[direction]
            if field_real[pos[1]][pos[0]].state != "#":
                allowed_moves[direction] = True

        if tile.can_turn == 2:
            allowed_moves[Directions.up] = False
            allowed_moves[Directions.down] = False
        elif tile.can_turn == 3:
            allowed_moves[Directions.down] = False
            pos = positions_to_check[Directions.up]
            if field_real[pos[1]][pos[0]].state == "=":
                allowed_moves[Directions.left] = False
                allowed_moves[Directions.right] = False

        allowed_moves[cant_choose_direction[self.direction]] = False
        best_direction = (None, 99999999)
        for direction in list(Directions):
            if not allowed_moves[direction]:
                continue
            pos = positions_to_check[direction]
            dist = sqrt((target[0] - pos[0]) ** 2 + (target[1] - pos[1]) ** 2)
            if dist < best_direction[1]:
                best_direction = (direction, dist)
        self.direction = best_direction[0] if best_direction[0] is not None else self.direction

    def set_frightened(self, timer):
        self.last_frightened = timer.time_game
        self.state = GhostStates.frightened

    def update_state(self, timer, dots_eaten):
        if self.state is GhostStates.killed and\
                (self.position[0] != KILLED_TARGET[0] or self.position[1] != KILLED_TARGET[1]):
            return
        if self.state == GhostStates.frightened:
            if timer.time_game - self.last_frightened < FRIGHTENED_TIME:
                return
        if timer.time_game % (SCATTER_TIME + CHASE_TIME) < SCATTER_TIME:
            self.state = GhostStates.scatter
        else:
            self.state = GhostStates.chase

    def move(self, field_real, timer, dots_eaten):
        self.update_state(timer, dots_eaten)
        if self.state is GhostStates.waiting:
            return
        self.move_n = (self.move_n + 1) % 2
        if self.state is GhostStates.frightened and self.move_n == 0:
            return

        moves = {Directions.up: (0, -1),
                 Directions.down: (0, 1),
                 Directions.left: (-1, 0),
                 Directions.right: (1, 0)}

        tile = field_real[self.position[1]][self.position[0]]
        if tile.state == ".":
            self.last_point = tuple(self.position)
        elif tile.state == "O":
            self.last_energetic = tuple(self.position)

        if field_real[self.last_point[1]][self.last_point[0]].state == ".":
            Printer.draw_dot(*PTSConverter.convert(self.last_point))
        if field_real[self.last_energetic[1]][self.last_energetic[0]].state == "O":
            Printer.draw_energetic(*PTSConverter.convert(self.last_energetic))

        self.clear()
        self.find_direction(field_real, None)
        self.anim = (self.anim + 1) % 2
        self.position[0] += moves[self.direction][0]
        self.position[1] += moves[self.direction][1]
        if self.state == GhostStates.killed:
            self.draw(Colors.black)
        elif self.state == GhostStates.frightened:
            color = [Colors.white, Colors.blue][self.anim]
            self.draw(color)
        else:
            self.draw(self.color)

    def check_pacman_intersection(self):
        return abs(self.pacman.position[1] - self.position[1]) < 2 and\
               abs(self.pacman.position[0] - self.position[0]) < 2
