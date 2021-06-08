from Menus.Menu import Menu
from config import CHARACTERS_FILENAME


class CharactersMenu(Menu):
    @staticmethod
    def use():
        CharactersMenu.draw(CHARACTERS_FILENAME)
        input()
