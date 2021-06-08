from Menus.Menu import Menu
from Printer import Printer
from Colors import Colors
import msvcrt
from config import HIGH_SCORES_FILENAME


class HighScoresMenuFinal(Menu):
    colors = [Colors.red, Colors.magenta, Colors.cyan, Colors.green, Colors.yellow]

    @staticmethod
    def use(player_score):
        scores = []
        with open(HIGH_SCORES_FILENAME, "r") as scores_file:
            for line in scores_file:
                record = line.strip("\n").split("-")
                scores.append((int(record[0]), record[1]))

            for i in range(10):
                if scores[i][0] < player_score:
                    break

            HighScoresMenuFinal.draw_prev(i)
            colors = HighScoresMenuFinal.colors
            player_name = HighScoresMenuFinal.get_player_name(18 + 7*i, player_score, colors[i % len(colors)])
            scores.append(None)
            scores[i+1:] = scores[i: -1]
            scores[i] = (player_score, player_name)
            HighScoresMenuFinal.draw_post(i)

        with open(HIGH_SCORES_FILENAME, "w") as scores_file:
            for i in range(10):
                line = f"{scores[i][0]}-{scores[i][1]}\n"
                scores_file.write(line)
        input()

    @staticmethod
    def get_player_name(y, player_score, color):
        x = 150 - len(str(player_score)) * 9
        Printer.print_word(str(player_score), x, y, color)
        x = 186
        inpn = 0
        player_name = ""
        while inpn != 13:
            inp = msvcrt.getch()
            inpn = ord(inp)
            try:
                inp = bytes.decode(inp)
                if inpn == 13:
                    return player_name
                elif inpn == 8:
                    if len(player_name) > 0:
                        x -= 9
                        player_name = player_name[:-1]
                        Printer.print_word(" ", x, y, color)
                elif inp.isalnum() and len(player_name) < 3:
                    Printer.print_word(inp, x, y, color)
                    x += 9
                    player_name = player_name + inp
            except UnicodeDecodeError:
                pass

    @staticmethod
    def draw_prev(n):
        Printer.clear_window()
        Printer.print_scores_base()
        with open(HIGH_SCORES_FILENAME, "r") as scores:
            colors = [Colors.red, Colors.magenta, Colors.cyan, Colors.green, Colors.yellow]
            y = 18
            for i, line in enumerate(scores):
                if i >= n:
                    return

                record = line.split("-")
                x = 150 - len(record[0]) * 9
                record = "    ".join(line.split("-"))
                Printer.print_word(record, x, y, colors[i % len(colors)])
                y += 7

    @staticmethod
    def draw_post(n):
        with open(HIGH_SCORES_FILENAME, "r") as scores:
            colors = [Colors.red, Colors.magenta, Colors.cyan, Colors.green, Colors.yellow]
            y = 18 + 7 * (n + 1)
            for i, line in enumerate(scores):
                if i <= n:
                    continue
                if i >= 10:
                    return

                record = line.split("-")
                x = 150 - len(record[0]) * 9
                record = "    ".join(line.split("-"))
                Printer.print_word(record, x, y, colors[i % len(colors)])
                y += 7
