import time
from distutils.core import setup_keywords

import serial
import matplotlib.pyplot as plt
from pygame import Vector3

import kinematics
import walk
import Bezier
import operations

class Control:
    def __init__(self, port):
        #self.walk_class = walk.WalkClass()
        self.port = port
        self.packet = []
        self.ser = serial.Serial(port, 1000000, timeout=1)
        self.calc = kinematics.calc()
        self.walk_class = walk.Walk_Class()

        #print(self.calc.calc_steps_local_coord([180, 0, -120], 2))
        self.current_gait = 1
        self.new_gait = 1
        self.origin_point = [180, 0, -80]
        self.test_point = []
        self.t = 0


    def close(self):
        self.ser.close()


    def test_move(self, leg, coord):
        #print(self.calc.just_calc(coord, leg, origin_point), leg)
        coord = self.calc.local_coord_to_abs_coord(coord, leg, self.origin_point)
        self.test_point.append(coord)
        #print(f"Leg: {leg}, coord: {coord}")

    def walk(self, walk_vector, turn_vector, gait):
        #print(f"Walk dir: {walk_dir}, speed: {walk_speed}, turn vector: {turn_vector}, gait: {gait}")
        self.new_gait = gait
        if self.current_gait != self.new_gait:
            # needs to home
            self.current_gait = self.new_gait

        if self.t > 0.5:
            self.t = self.t % 1
        else:
            self.t = self.t + 0.02
        walk_vector[0] = operations.map_value(walk_vector[0], -1, 1, -100, 100)
        walk_vector[1] = operations.map_value(walk_vector[1], -1, 1, -100, 100)
        turn_vector[0] = operations.map_value(turn_vector[0], -1, 1, -100, 100)
        turn_vector[1] = operations.map_value(turn_vector[1], -1, 1, -100, 100)

        points = self.walk_class.walk(walk_vector, turn_vector, gait)
        self.test_move(1, points[0])
        self.test_move(2, points[1])
        self.test_move(3, points[2])
        self.test_move(4, points[3])
        self.test_move(5, points[4])
        self.test_move(6, points[5])


    def draw(self):
        print(self.test_point)
        plot_3d_points(self.test_point)

    def reset(self):
        self.test_point = []




def plot_3d_points(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Entpacken der Punkte in separate Listen für x, y und z
    x_vals = [point[0] for point in points]
    y_vals = [point[1] for point in points]
    z_vals = [point[2] for point in points]

    # Scatter plot der Punkte
    ax.scatter(x_vals, y_vals, z_vals)

    # Achsenbeschriftungen
    ax.set_xlabel('X Achse')
    ax.set_ylabel('Y Achse')
    ax.set_zlabel('Z Achse')

    # Titel setzen
    ax.set_title('3D Punkte Plot')

    # Bestimmen der gleichen Grenzen für alle Achsen
    max_range = max(max(x_vals) - min(x_vals), max(y_vals) - min(y_vals), max(z_vals) - min(z_vals))

    # Mittelpunkt der Achsen
    mid_x = (max(x_vals) + min(x_vals)) * 0.5
    mid_y = (max(y_vals) + min(y_vals)) * 0.5
    mid_z = (max(z_vals) + min(z_vals)) * 0.5

    # Setzen der gleichen Grenzen für alle Achsen
    ax.set_xlim(mid_x - max_range * 0.5, mid_x + max_range * 0.5)
    ax.set_ylim(mid_y - max_range * 0.5, mid_y + max_range * 0.5)
    ax.set_zlim(mid_z - max_range * 0.5, mid_z + max_range * 0.5)

    # Zeige den Plot an
    plt.show()

