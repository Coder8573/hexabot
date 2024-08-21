import time
import serial
import matplotlib.pyplot as plt

import kinematics
import walk
import Bezier


class Control:
    def __init__(self, port):
        self.port = port
        self.packet = []
        self.ser = serial.Serial(port, 1000000, timeout=1)
        self.calc = kinematics.calc()

        self.test_point = []


    def close(self):
        self.ser.close()


    def test(self):
        #point = [(-80, 0, 0), (-80, 0, 80), (80, 0, 0)]
        point = [(-80, 0, 0), (80, 0, 0)]
        for i in range(0, 101):
            t = i/100
            self.points.append(Bezier.get_point_on_curve_3(point, len(point), t))

        print(self.points)
        plot_3d_points(self.points)





    def move(self, leg, coord):
        coord = self.calc.local_coord_to_abs_coord(coord, leg)
        self.test_point.append(coord)
        print(f"Leg: {leg}, coord: {coord}")


    def walk(self, dir, speed, turn_strength, turn_dir, gait):
        print(f"Walk dir: {dir}, speed: {speed}, trun strength: {turn_strength}, turn dir: {turn_dir}, gait: {gait}")
        speed = max()
        self.new_gait = gait
        if self.current_gait != self.new_gait:
            # needs to home
            self.current_gait = self.new_gait
        self.move(1, walk.gen_point(1, dir, speed, turn_dir, turn_strength, gait))
        self.move(2, walk.gen_point(2, dir, speed, turn_dir, turn_strength, gait))
        self.move(3, walk.gen_point(3, dir, speed, turn_dir, turn_strength, gait))
        self.move(4, walk.gen_point(4, dir, speed, turn_dir, turn_strength, gait))
        self.move(5, walk.gen_point(5, dir, speed, turn_dir, turn_strength, gait))
        self.move(6, walk.gen_point(6, dir, speed, turn_dir, turn_strength, gait))





    def draw(self):
        plot_3d_points(self.points)



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


