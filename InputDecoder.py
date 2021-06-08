import msvcrt
from Directions import Directions


class InputDecoder(object):
    directions = {"w": Directions.up,
                  "s": Directions.down,
                  "a": Directions.left,
                  "d": Directions.right,
                  # for arrows:
                  "H": Directions.up,
                  "P": Directions.down,
                  "K": Directions.left,
                  "M": Directions.right,
                  }

    @staticmethod
    def get_direction():
        if msvcrt.kbhit() != 1:
            return None

        direction = msvcrt.getch()
        try:  # if using "w", "a", "s" & "d"
            direction = bytes.decode(direction)
            direction = direction.lower()
        except UnicodeDecodeError:  # if using arrows
            direction = msvcrt.getch()
            direction = bytes.decode(direction)
        return InputDecoder.directions.get(direction)

    @staticmethod
    def get_main_menu_input():
        inp = msvcrt.getch()
        inpn = ord(inp)
        try:  # if using "w", "a", "s" & "d"
            inp = bytes.decode(inp)
        except UnicodeDecodeError:  # if using arrows
            inp = msvcrt.getch()
            inp = bytes.decode(inp)
        direction = InputDecoder.directions.get(inp)
        return direction, inpn == 13

