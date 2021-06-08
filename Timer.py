class Timer:
    def __init__(self):
        self.time_game = 0

    def restart(self):
        self.time_game = 0

    def update(self):
        self.time_game += 1
