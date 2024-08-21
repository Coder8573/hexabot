import math

# home_pos = Vector(0, 5, 6)

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def change(self, new_x, new_y, new_z):
        self.x = new_x
        self.y = new_y
        self.z = new_z
