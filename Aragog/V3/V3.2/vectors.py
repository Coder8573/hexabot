import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def change(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def to_string(self):
        return f"({self.x} | {self.y} | {self.z})"

    def add(self, Vector2):
        self.x = self.x + Vector2.x
        self.y = self.y + Vector2.y

    def multi_with_val(self, val):
        self.x = self.x * val
        self.y = self.y * val

    def multi_with_vector(self, Vector2):
        self.x = self.x * Vector2.x
        self.y = self.y * Vector2.y

    def rotate(self, angle, pivot):
        rad = math.radians(angle)
        self.x = self.x - pivot.x
        self.y = self.y - pivot.y

        x_rotated = self.x * math.cos(rad) - self.y * math.sin(rad)
        y_rotated = self.x * math.sin(rad) - self.y * math.cos(rad)

        self.x = x_rotated + pivot.x
        self.y = y_rotated + pivot.y


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def change(self, new_x, new_y, new_z):
        self.x = new_x
        self.y = new_y
        self.z = new_z

    def to_string(self):
        return f"({self.x} | {self.y} | {self.z})"

    def add(self, Vector3):
        self.x = self.x + Vector3.x
        self.y = self.y + Vector3.y
        self.z = self.z + Vector3.z

    def multi_with_val(self, val):
        self.x = self.x * val
        self.y = self.y * val
        self.z = self.z * val

    def multi_with_vector(self, Vector3):
        self.x = self.x * Vector3.x
        self.y = self.y * Vector3.y
        self.z = self.z * Vector3.z

    def rotate(self, angle, pivot):
        rad = math.radians(angle)
        self.x = self.x - pivot.x
        self.y = self.y - pivot.y

        x_rotated = self.x * math.cos(rad) - self.y * math.sin(rad)
        y_rotated = self.x * math.sin(rad) - self.y * math.cos(rad)

        self.x = x_rotated + pivot.x
        self.y = y_rotated + pivot.y