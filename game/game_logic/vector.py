import numpy as np

class Vector2(object):

    def __init__(self, head=np.array([0., 0.]), tail=np.array([0., 0.]), angle=0, mag=0, unit=np.array([0., 0.])):
        self.head = head
        self.tail = tail
        self.angle = angle
        self.mag = mag
        self.unit = unit

    # give a new head/tail and update all attributes
    def set(self, head, tail):
        self.tail[0] = tail[0]
        self.tail[1] = tail[1]
        self.head[0] = head[0]
        self.head[1] = head[1]

        delta_x = abs(self.tail[0] - self.head[0])
        delta_y = abs(self.tail[1] - self.head[1])

        left = self.head[0] < self.tail[0]
        up = self.head[1] < self.tail[1]
        
        # magnitude from centered on origin
        centered = np.array([delta_x, delta_y])
        self.mag = np.sqrt(centered.dot(centered))
        self.angle = np.arctan2(delta_y, delta_x)

        # unit vector, corrected direction
        self.unit = np.array([np.cos(self.angle), np.sin(self.angle)])
        if left: self.unit[0] *= -1
        if up: self.unit[1] *= -1
