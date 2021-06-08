from Menus.Menu import Menu
from Printer import Printer
from Colors import Colors
from config import HIGH_SCORES_FILENAME


class HighScoresMenu(Menu):
    @staticmethod
    def use():
        HighScoresMenu.draw(HIGH_SCORES_FILENAME)
        input()

    @staticmethod
    def draw(filename):
        Printer.clear_window()
        Printer.print_scores_base()
        with open(HIGH_SCORES_FILENAME, "r") as scores:
            colors = [Colors.red, Colors.magenta, Colors.cyan, Colors.green, Colors.yellow]
            y = 18
            for n, line in enumerate(scores):
                if n >= 10:
                    return

                record = line.split("-")
                x = 150 - len(record[0]) * 9
                record = "    ".join(line.split("-"))
                Printer.print_word(record, x, y, colors[n % len(colors)])
                y += 7
