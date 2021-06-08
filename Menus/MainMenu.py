from Cursor import Cursor, CursorPositions
from InputDecoder import InputDecoder
from Menus.Menu import Menu
from Menus.CharactersMenu import CharactersMenu
from Menus.HighScoresMenu import HighScoresMenu
from Printer import Printer
from sys import exit
from config import MAIN_MENU_FILENAME


class MainMenu(Menu):
    cursor = Cursor()

    @staticmethod
    def use():
        MainMenu.cursor.position = CursorPositions.play_game
        MainMenu.draw(MAIN_MENU_FILENAME)
        while True:
            direction, is_enter = InputDecoder.get_main_menu_input()

            if is_enter:
                if MainMenu.cursor.position is CursorPositions.play_game:
                    Printer.clear_window()
                    return
                if MainMenu.cursor.position is CursorPositions.characters:
                    CharactersMenu.use()
                elif MainMenu.cursor.position is CursorPositions.high_scores:
                    HighScoresMenu.use()
                else:
                    exit()
                MainMenu.draw(MAIN_MENU_FILENAME)
                MainMenu.cursor.position = CursorPositions.play_game

            if direction is None:
                continue
            MainMenu.cursor.move(direction)
