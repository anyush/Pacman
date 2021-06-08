import os
from Colors import Colors
from config import GRAPHICS_DIR, ENERGETIC_FILENAME, MAP_GRAPHICS_FILENAME, LIVES_FILENAME


class Printer(object):
    @staticmethod
    def set_default_colors():
        print("\033[37;40m")

    @staticmethod
    def clear_window():
        print("\033[49m", end='')
        os.system('cls')

    @staticmethod
    def print_word(word, x, y, color):
        word = word.strip("\n")

        x -= 9
        for symbol in word:
            x += 9
            if symbol == " ":
                for i in range(5):
                    print(f"\033[{y + i};{x}H" + Colors.black.value + "       ")
                continue
            with open(GRAPHICS_DIR + symbol.upper() + ".txt") as symbol_file:
                for i, line in enumerate(symbol_file):
                    line = line.strip("\n")
                    line = line.replace("#", color.value + "#")
                    line = line.replace(" ", Colors.black.value + " ")
                    print(f"\033[{y + i};{x}H" + line + Colors.black.value, end="")

    @staticmethod
    def print_map():
        with open(MAP_GRAPHICS_FILENAME, "r") as map_file:
            for line in map_file:
                print(line, end="\033[40m")

    @staticmethod
    def print_score(score):
        Printer.print_word("        ", 56, 95, Colors.black)
        Printer.print_word(str(score), 56, 95, Colors.white)

    @staticmethod
    def print_lives(lives):
        x = 186
        y = 95
        Printer.print_word("   ", x, y, Colors.yellow)
        if lives > 0:
            for i in range(lives - 1):
                with open(LIVES_FILENAME, "r") as life_file:
                    for j, line in enumerate(life_file):
                        line = line.replace("#", Colors.yellow.value + "#")
                        line = line.replace(" ", Colors.black.value + " ")
                        print(f"\033[{y + j};{x}H" + line)
                x += 9

    @staticmethod
    def clear_tile(x, y):
        print(f"\033[49m\033[{y};{x}H       \033[{y+1};{x}H       \033[{y+2};{x}H       ")

    @staticmethod
    def draw_dot(x, y):
        print(Colors.magenta.value + f"\033[{y + 1};{x + 3}H\033[35;45m#")

    @staticmethod
    def draw_energetic(x, y):
        with open(ENERGETIC_FILENAME, "r") as bonus_file:
            for i, line in enumerate(bonus_file):
                line = line.replace("#", Colors.magenta.value + "#")
                line = line.replace(" ", Colors.black.value + " ")
                print(f"\033[{y+i};{x}H" + line)



    @staticmethod
    def print_game_over():
        for i in range(5):
            print(f"\033[30;40m\033[{55+i};86H                                    " +
                  "                                           ")
        Printer.print_word("game over", 87, 55, Colors.red)
        print("\033[34;44m\033[54;87H####################################" +
              "###########################################\033[55;86H#\033[55;166H#" +
              "\033[56;86H#\033[56;166H#\033[57;86H#\033[57;166H#\033[58;86H#\033[58;166H#"
              "\033[59;86H#\033[59;166H#\033[44m\033[60;87H##################################"
              "#############################################")

    @staticmethod
    def print_scores_base():
        print(Colors.blue.value, end='')
        for i in range(252):
            print("#", end='')
        print()
        for i in range(97):
            print("#\033[49m", end='')
            for j in range(250):
                print(" ", end='')
            print("\033[44m#")
        for i in range(252):
            print("#", end='')
        Printer.print_word("10 best players", 42, 4, Colors.white)
        Printer.print_word("Rank    score  initial", 33, 11, Colors.green)
        Printer.print_word("1st", 42, 18, Colors.red)
        Printer.print_word("2nd", 42, 25, Colors.magenta)
        Printer.print_word("3rd", 42, 32, Colors.cyan)
        Printer.print_word("4th", 42, 39, Colors.green)
        Printer.print_word("5th", 42, 46, Colors.yellow)
        Printer.print_word("6th", 42, 53, Colors.red)
        Printer.print_word("7th", 42, 60, Colors.magenta)
        Printer.print_word("8th", 42, 67, Colors.cyan)
        Printer.print_word("9th", 42, 74, Colors.green)
        Printer.print_word("10th", 33, 81, Colors.yellow)
