
class Grid(object):

    # map the grid to the entire display
    def __init__(self, component, width=1, height=1):
        self.width = component.width // width
        self.height = component.height // height

    # return top left pixel of given x, y coord on the grid
    def get_pixel(self, x, y):
        return (self.width * (x - 1), self.height * (y - 1))

class Relative(object):

    def __init__(self, component):

        self.x = component.anchored_loc[0]
        self.y = component.anchored_loc[1]
        self.width = component.width
        self.height = component.height

        # the pixel locations of the grid intersections
        self.north = (self.x + self.width / 2, self.y)
        self.northeast = (self.x + self.width, self.y)
        self.east = (self.x + self.width, self.y + self.height / 2)
        self.southeast = (self.x + self.width, self.y + self.height)
        self.south = (self.x + self.width / 2, self.y + self.height)
        self.southwest = (self.x, self.y + self.height)
        self.west = (self.x, self.y + self.height / 2)
        self.northwest = (self.x, self.y)

        self.center = (self.x + self.width / 2, self.y + self.height / 2)
