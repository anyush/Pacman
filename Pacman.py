from Directions import Directions
from Colors import Colors
from InputDecoder import InputDecoder
from PointToScreenConverter import PointToScreenConverter as PTSConverter
from config import PACMAN_START_POSITION, PACMAN_CLOSED_FILENAME, PACMAN_UP_FILENAME, PACMAN_DOWN_FILENAME,\
    PACMAN_LEFT_FILENAME, PACMAN_RIGHT_FILENAME


class Pacman:
    textures = {}

    def __init__(self):
        self.direction = Directions.right
        self.next_move = Directions.right
        self.anim = 0
        self.position = list(PACMAN_START_POSITION)
        self.stopped = False
        self.init_textures()

    def init_textures(self):
        tex_names = {None: PACMAN_CLOSED_FILENAME,
                     Directions.up: PACMAN_UP_FILENAME,
                     Directions.down: PACMAN_DOWN_FILENAME,
                     Directions.left: PACMAN_LEFT_FILENAME,
                     Directions.right: PACMAN_RIGHT_FILENAME
                     }
        for tex_name in tex_names.keys():
            with open(tex_names[tex_name], "r") as tex_file:
                texture = "".join(list(tex_file))
                self.textures[tex_name] = texture

    def reset(self):
        self.position = list(PACMAN_START_POSITION)
        self.anim = 0
        self.direction = Directions.right
        self.next_move = Directions.right

    def clear(self):
        texture = self.textures[None] if self.anim == 0 else self.textures[self.direction]
        coords = PTSConverter.convert(self.position)
        print(Colors.black.value)
        for i, line in enumerate(texture.split("\n")):
            print(f"\033[{coords[1] + i};{coords[0]}H" + line)

    def draw(self):
        texture = self.textures[None] if self.anim == 0 else self.textures[self.direction]
        texture = texture.replace("#", Colors.yellow.value + "#")
        texture = texture.replace(" ", Colors.black.value + " ")
        coords = PTSConverter.convert(self.position)
        for i, line in enumerate(texture.split("\n")):
            print(f"\033[{coords[1] + i};{coords[0]}H" + line)

    def check_direction(self, field_real):
        allowed_moves = {Directions.up: False,
                         Directions.down: False,
                         Directions.left: False,
                         Directions.right: False}
        cells_to_check = {Directions.up: field_real[self.position[1] - 3][self.position[0]],
                          Directions.down: field_real[self.position[1] + 3][self.position[0]],
                          Directions.left: field_real[self.position[1]][self.position[0] - 3],
                          Directions.right: field_real[self.position[1]][self.position[0] + 3]}

        for direction in list(Directions):
            if cells_to_check[direction].state != "#":
                allowed_moves[direction] = True

        next_move = InputDecoder.get_direction()
        if next_move is not None:
            self.next_move = next_move
        if allowed_moves[self.next_move]:
            self.direction = self.next_move
            self.stopped = False
        if not allowed_moves[self.direction]:
            self.stopped = True

    def move(self, field_real):
        moves = {Directions.up: (0, -1),
                 Directions.down: (0, 1),
                 Directions.left: (-1, 0),
                 Directions.right: (1, 0)}

        self.clear()
        self.check_direction(field_real)
        if not self.stopped:
            self.anim = (self.anim + 1) % 2
            self.position[0] += moves[self.direction][0]
            self.position[1] += moves[self.direction][1]
        self.draw()
