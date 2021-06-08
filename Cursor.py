from enum import Enum
from Directions import Directions
from Colors import Colors
from Printer import Printer
from config import CURSOR_FILENAME, CURSOR_0_POSITION, CURSOR_1_POSITION, CURSOR_2_POSITION, CURSOR_3_POSITION


class CursorPositions(Enum):
    play_game = 0
    high_scores = 1
    characters = 2
    exit = 3


class Cursor(object):
    position_coords = {CursorPositions.play_game:   CURSOR_0_POSITION,
                       CursorPositions.high_scores: CURSOR_1_POSITION,
                       CursorPositions.characters:  CURSOR_2_POSITION,
                       CursorPositions.exit:        CURSOR_3_POSITION}

    def __init__(self):
        self.position = CursorPositions.play_game

    def draw(self, color):
        print(color.value)
        with open(CURSOR_FILENAME, "r") as cursor_file:
            for i, line in enumerate(cursor_file):
                line = line.replace("#", color.value + "#")
                line = line.replace(" ", Colors.black.value + " ")
                print(f"\033[{self.position_coords[self.position][1]+i};" +
                      f"{self.position_coords[self.position][0]}H" + line)
        Printer.set_default_colors()

    def move(self, direction):
        if not ((self.position is not CursorPositions.play_game and direction is Directions.up) or
                (self.position is not CursorPositions.exit and direction is Directions.down)):
            return

        self.draw(Colors.black)
        self.position = CursorPositions(self.position.value+1) if direction is Directions.down else \
            CursorPositions(self.position.value-1)
        self.draw(Colors.blue)
