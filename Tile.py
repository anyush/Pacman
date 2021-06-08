class Tile:
    def __init__(self, state, y, x):
        self.state = state
        self.y = y
        self.x = x
        self.can_turn = 0

    def convert(self):
        if self.state == 'X':
            self.can_turn = 1
            self.state = '.'
        elif self.state == '+':
            self.can_turn = 1
            self.state = ' '
        elif self.state == 'Q':
            self.can_turn = 1
            self.state = 'O'
        elif self.state == '-':
            self.can_turn = 2
            self.state = ' '
        elif self.state == '/':
            self.can_turn = 2
            self.state = '.'
        elif self.state == 'E':
            self.can_turn = 3
            self.state = ' '
