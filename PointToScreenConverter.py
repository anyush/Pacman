class PointToScreenConverter(object):
    @staticmethod
    def convert(pos):
        x, y = pos
        return 3*x+2, y+1
