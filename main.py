import os
import time
import colorama
import msvcrt
from Pacman import Pacman
from Printer import Printer
from Ghost import GhostStates
from Ghost.Blinky import Blinky
from Ghost.Pinky import Pinky
from Ghost.Inky import Inky
from Ghost.Clyde import Clyde
from Menus.MainMenu import MainMenu
from Menus.HighScoresMenuFinal import HighScoresMenuFinal
from Fruit import Fruit
from EventHandler import EventHandler
from Timer import Timer
from Tile import Tile
from config import MAP_FILENAME


class Game:
    def __init__(self):
        self.field_real = [[Tile("", y, x) for x in range(84)] for y in range(0, 91)]
        self.timer = Timer()
        self.pacman = Pacman()

        blinky = Blinky(self.pacman)
        pinky = Pinky(self.pacman)
        inky = Inky(self.pacman, blinky)
        clyde = Clyde(self.pacman)
        self.ghosts = (blinky, pinky, inky, clyde)
        self.fruit = Fruit()
        self.score = 0
        self.speed = 0.1
        self.lvl = 1
        self.dots_eaten = 0
        self.ghosts_eaten = 0
        self.lives = 3
        self.ghost_state = GhostStates.scatter
        self.n = 0
        self.timer.restart()
        self.extra_life_given = False

    def load_map(self):
        with open(MAP_FILENAME, "r") as infile:
            for y, line in enumerate(infile):
                line = line.strip("\n")
                for x, symbol in enumerate(line):
                    self.field_real[y][x].state = symbol
                    self.field_real[y][x].convert()

    def print_start(self):
        print("\033[37;49mPlease change the font to smallest and press any key. (use only english-symbol layout)")
        msvcrt.getch()
        Printer.clear_window()

    def move(self):
        self.fruit.touch(self.dots_eaten, self.timer, self.field_real)
        self.pacman.move(self.field_real)
        for ghost in self.ghosts:
            ghost.move(self.field_real, self.timer, self.dots_eaten)
        self.n = (self.n+1) % 2
        time.sleep(self.speed)

    def play(self):
        self.print_start()
        os.system('mode con: cols=253 lines=101')
        while True:
            self.load_map()
            MainMenu.use()
            Printer.print_map()
            Printer.print_lives(self.lives)
            Printer.print_score(self.score)
            while self.lives > 0:
                self.move()
                self.timer.update()
                EventHandler.handle_events(self)
            Printer.print_game_over()
            time.sleep(3)
            HighScoresMenuFinal.use(self.score)


colorama.init()
gm = Game()
gm.play()
colorama.deinit()
