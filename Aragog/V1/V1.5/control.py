import serial
import matplotlib.pyplot as plt

import kinematics
from walk import Walk_Class


class Control:
    def __init__(self, port):
        self.port = port
        self.packet = []
        self.ser = serial.Serial(port, 1000000, timeout=1)
        self.calc = kinematics.calc()
        self.current_gait = 1
        self.new_gait = 1
        self.origin_point = [180, 0, -80]
        self.walk_class = Walk_Class(self.origin_point)
        self.last_points = [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]]
        self.new_points = [[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]]

        self.test_point = []


    def close(self):
        self.ser.close()


    def move(self, leg, coord):
        coord = self.calc.local_coord_to_abs_coord(coord, leg, self.origin_point)
        self.test_point.append(coord)
        #print(f"Leg: {leg}, coord: {coord}")


    def walk(self, joy1, joy2, gait):
        #print(f"Walk dir: {walk_dir}, speed: {walk_speed}, trun vector: {turn_vector}, gait: {gait}")
        self.new_gait = gait
        if self.current_gait != self.new_gait:
            # needs to home
            self.current_gait = self.new_gait
            for i in range(6):
                self.last_points[i] = self.origin_point
        #print(self.last_points)
        self.new_points[0] = self.walk_class.gen_point(1, joy1, joy2, gait, self.origin_point)
        self.new_points[1] = self.walk_class.gen_point(2, joy1, joy2, gait, self.origin_point)
        self.new_points[2] = self.walk_class.gen_point(3, joy1, joy2, gait, self.origin_point)
        self.new_points[3] = self.walk_class.gen_point(4, joy1, joy2, gait, self.origin_point)
        self.new_points[4] = self.walk_class.gen_point(5, joy1, joy2, gait, self.origin_point)
        self.new_points[5] = self.walk_class.gen_point(6, joy1, joy2, gait, self.origin_point)
        self.move(1, self.new_points[0])
        self.move(2, self.new_points[1])
        self.move(3, self.new_points[2])
        self.move(4, self.new_points[3])
        self.move(5, self.new_points[4])
        self.move(6, self.new_points[5])
        self.last_points = self.new_points


    def draw(self):
        print(self.test_point)
        plot_3d_points(self.test_point)

    def reset(self):
        self.test_point = []
        self.last_points = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.new_points = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]



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


