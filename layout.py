
from config import settings

class Grid(object):

    # map the grid to the entire display
    def __init__(self, width=1, height=1):
        self.width = settings.display_size // width
        self.height = settings.display_size // height

    # return top left pixel of given x, y coord on the grid
    def get_pixel(self, x, y):
        return (self.width * (x - 1), self.height * (y - 1))

class Relative(object):

    # the pixel locations of the grid intersections
    north = (settings.display_size / 2, 0)
    northeast = (settings.display_size, 0)
    east = (settings.display_size, settings.display_size / 2)
    southeast = (settings.display_size, settings.display_size)
    south = (settings.display_size / 2, settings.display_size)
    southwest = (0, settings.display_size)
    west = (0, settings.display_size / 2)
    northwest = (0, 0)

    center = (settings.display_size / 2, settings.display_size / 2)
