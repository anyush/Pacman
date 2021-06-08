from config import FRUIT_POSITION, FRUIT_TIME, FRUIT_FILENAME, FRUIT_DOTS_EATEN_APPEAR
from Colors import Colors


class Fruit(object):
    def __init__(self):
        self.active = False
        self.appear_n_dots = FRUIT_DOTS_EATEN_APPEAR
        self.last_appearance_time = 0

    def touch(self, dots_eaten, timer, field_real):
        if dots_eaten in self.appear_n_dots:
            field_real[FRUIT_POSITION[1]][FRUIT_POSITION[0]].state = "*"
            self.last_appearance_time = timer.time_game
            self.active = True
        elif timer.time_game - self.last_appearance_time > FRUIT_TIME:
            field_real[FRUIT_POSITION[1]][FRUIT_POSITION[0]].state = " "
            self.active = False
        if self.active:
            Fruit.draw()

    @staticmethod
    def draw():
        x = 129
        y = 52
        with open(FRUIT_FILENAME, "r") as fruit_file:
            for i, line in enumerate(fruit_file):
                line = line.replace("G", Colors.green.value + "#")
                line = line.replace("R", Colors.red.value + "#")
                line = line.replace(" ", Colors.black.value + " ")
                print(f"\033[{y+i};{x}H" + line)
