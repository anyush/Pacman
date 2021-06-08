from enum import Enum


class Colors(Enum):
    red = "\033[31;41m"
    green = "\033[32;42m"
    yellow = "\033[33;43m"
    blue = "\033[34;44m"
    magenta = "\033[35;45m"
    cyan = "\033[36;46m"
    white = "\033[37;47m"
    black = "\033[30;40m"
