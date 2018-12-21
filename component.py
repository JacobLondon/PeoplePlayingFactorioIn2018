
from config import settings
from constants import Anchor, Font, Color
from layout import Grid

class Component(object):

    def __init__(self, interface):

        self.interface = interface
        self.loc = (0, 0)
        self.anchored_loc = (0, 0)
        self.width = 0
        self.height = 0
        self.container = []

        self.text = ''
        self.font = Font.standard
        self.foreground = Color.foreground
        self.background = Color.background
        self.anchor = Anchor.northwest

    # set the relative location determined by the anchor used
    def set_anchor(self):
        self.width, self.height = self.font.size(self.text)

        if self.anchor == Anchor.northwest:
            self.anchored_loc = self.loc
        elif self.anchor == Anchor.northeast:
            self.anchored_loc = (self.loc[0] - self.width, self.loc[1])
        elif self.anchor == Anchor.southwest:
            self.anchored_loc = (self.loc[0], self.loc[1] - self.height)
        elif self.anchor == Anchor.southeast:
            self.anchored_loc = (self.loc[0] - self.width, self.loc[1] - self.height)
        elif self.anchor == Anchor.center:
            self.anchored_loc = (self.loc[0] - self.width / 2, self.loc[1] - self.height / 2)

    # determine if the coordinates are inside of a given component
    def in_component(self, x, y):
        return all(self.anchored_loc[0] <= x <= self.anchored_loc[0] + self.width,
                   self.anchored_loc[1] <= y <= self.anchored_loc[1] + self.height)
