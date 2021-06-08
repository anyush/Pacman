from abc import ABC, abstractmethod
from Printer import Printer


class Menu(ABC):
    @staticmethod
    @abstractmethod
    def use(*args):
        pass

    @staticmethod
    def draw(filename):
        Printer.clear_window()
        with open(filename, "r") as file:
            for line in file:
                print(line, end='')
