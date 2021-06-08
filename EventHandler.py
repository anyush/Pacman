from Printer import Printer
from Ghost import GhostStates
from PointToScreenConverter import PointToScreenConverter as PTSConverter
import time
from config import POINTS_PER_DOT, EXTRA_LIFE_POINTS_N, DOTS_ON_LEVEL, PER_LEVEL_SPEED_UP, POINTS_PER_ENERGETIC, \
    BASE_POINTS_PER_FRUIT, FIRST_GHOST_EATEN_POINTS, NEXT_GHOST_EATEN_MULTIPLIER


class EventHandler(object):
    @staticmethod
    def handle_events(game):
        if game.field_real[game.pacman.position[1]][game.pacman.position[0]].state == '.':
            EventHandler.dot_eaten(game)

        if game.field_real[game.pacman.position[1]][game.pacman.position[0]].state == 'O':
            EventHandler.energetic_eaten(game)

        if game.field_real[game.pacman.position[1]][game.pacman.position[0]].state == '*':
            EventHandler.fruit_eaten(game)

        for ghost in game.ghosts:
            if ghost.check_pacman_intersection():
                EventHandler.pacman_ghost_collision(game, ghost)

        if game.score == EXTRA_LIFE_POINTS_N and not game.extra_life_given:
            EventHandler.give_extra_life(game)

    @staticmethod
    def dot_eaten(game):
        game.score += POINTS_PER_DOT
        game.dots_eaten += 1
        game.field_real[game.pacman.position[1]][game.pacman.position[0]].state = ' '
        Printer.print_score(game.score)

        if game.dots_eaten == DOTS_ON_LEVEL:
            Printer.clear_window()
            Printer.print_map()
            Printer.print_score(game.score)
            Printer.print_lives(game.lives)
            game.pacman.reset()
            for ghost in game.ghosts:
                ghost.reset()
            game.dots_eaten = 0
            game.timer.restart()
            game.load_map()
            game.speed /= PER_LEVEL_SPEED_UP
            game.lvl += 1

    @staticmethod
    def energetic_eaten(game):
        for ghost in game.ghosts:
            if ghost.state is not GhostStates.killed and \
                    ghost.state is not GhostStates.waiting:
                ghost.set_frightened(game.timer)

        game.field_real[game.pacman.position[1]][game.pacman.position[0]].state = ' '
        game.score += POINTS_PER_ENERGETIC
        game.ghosts_eaten = 0
        Printer.print_score(game.score)
        coords = PTSConverter.convert(game.pacman.position)
        Printer.clear_tile(*coords)

    @staticmethod
    def fruit_eaten(game):
        game.fruit.active = False
        game.field_real[game.pacman.position[1]][game.pacman.position[0]].state = ' '
        game.score += BASE_POINTS_PER_FRUIT * game.lvl
        Printer.print_score(game.score)

    @staticmethod
    def pacman_ghost_collision(game, ghost):
        if ghost.state is GhostStates.frightened:
            ghost.state = GhostStates.killed
            game.score += FIRST_GHOST_EATEN_POINTS * (NEXT_GHOST_EATEN_MULTIPLIER ** game.ghosts_eaten)
            game.ghosts_eaten += 1
            Printer.print_score(game.score)
        elif ghost.state is not GhostStates.killed:
            game.pacman.clear()
            for ghost in game.ghosts:
                if ghost.state is not GhostStates.waiting:
                    ghost.clear()
            game.pacman.reset()
            for ghost in game.ghosts:
                ghost.reset()
            game.lives -= 1
            Printer.print_lives(game.lives)
            time.sleep(2)

    @staticmethod
    def give_extra_life(game):
        game.extra_life_given = True
        game.lives += 1
        Printer.print_lives(game.lives)
