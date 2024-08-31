import time
import serial
import matplotlib.pyplot as plt

import kinematics
import walk


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

    def move(self, leg, coord):  # , direction, speed, rotation
        steps = self.calc.steps_local_coord(coord, leg)
        if not self.packet:
            self.packet = [0xFF, 0xFF, 0xFE, 0, 0x83, 0x2A, 0x06,
                           (leg*3)-2, self.calc_low_byte(steps[0]), self.calc_high_byte(steps[0]), 0X00, 0X00, 0X00, 0X00,
                           (leg*3)-1, self.calc_low_byte(steps[1]), self.calc_high_byte(steps[1]), 0X00, 0X00, 0X00, 0X00,
                           (leg*3), self.calc_low_byte(steps[2]), self.calc_high_byte(steps[2]), 0X00, 0X00, 0X00, 0X00]
        else:
            self.packet.extend([
              (leg * 3) - 2, self.calc_low_byte(steps[0]), self.calc_high_byte(steps[0]), 0X00, 0X00, 0X00, 0X00,
              (leg * 3) - 1, self.calc_low_byte(steps[1]), self.calc_high_byte(steps[1]), 0X00, 0X00, 0X00, 0X00,
              (leg * 3), self.calc_low_byte(steps[2]), self.calc_high_byte(steps[2]), 0X00, 0X00, 0X00, 0X00])
        #self.last_points[leg-1] = coord

    def execute_move(self):
        #print(f"""{self.packet}self.packet""")
        #print(f"""{packet}"Test""")
        self.packet[3] = len(self.packet)-1
        #print(len(self.packet))
        self.packet.append(self.calculate_checksum(self.packet))
        self.ser.write(bytearray(self.packet))
        self.ser.write(bytearray(self.packet))
        #print(f"""{self.packet}"Test2""")
        #time.sleep(0.05)
        self.packet = []

    def close(self):
        self.ser.close()

    def calculate_checksum(self, data):
        checksum = sum(data) & 0xFF
        return (~checksum) & 0xFF

    def calc_low_byte(self, data):
        return data & 0xFF

    def calc_high_byte(self, data):
        return (data >> 8) & 0xFF


    def test_move(self, leg, coord):
        #print(self.calc.just_calc(coord, leg, origin_point), leg)
        coord = self.calc.local_coord_to_abs_coord(coord, leg, self.origin_point)
        #coord = self.calc.calc_steps_local_coord(coord, leg)
        self.test_point.append(coord)
        #print(f"Leg: {leg}, coord: {coord}")

    def walk(self, joy1, joy2, gait):
        #print(f"Walk dir: {walk_dir}, speed: {walk_speed}, turn vector: {turn_vector}, gait: {gait}")
        self.new_gait = gait
        if self.current_gait != self.new_gait:
            # needs to home
            self.current_gait = self.new_gait

        #walk_vector[0] = operations.map_value(walk_vector[0], -1, 1, -100, 100)
        #walk_vector[1] = operations.map_value(walk_vector[1], -1, 1, -100, 100)
        #turn_vector[0] = operations.map_value(turn_vector[0], -1, 1, -100, 100)
        #turn_vector[1] = operations.map_value(turn_vector[1], -1, 1, -100, 100)

        points = self.walk_class.walk(joy1, joy2, gait)
        #self.test_move(1, points[0])
        #self.test_move(2, points[1])
        #self.test_move(3, points[2])
        #self.test_move(4, points[3])
        #self.test_move(5, points[4])
        #self.test_move(6, points[5])

        self.move(1, points[0])
        self.move(2, points[1])
        self.move(3, points[2])
        self.move(4, points[3])
        self.move(5, points[4])
        self.move(6, points[5])
        self.execute_move()

    def home(self, coord=(150, 0, -160)):
        pass
        self.move(1, [95, 0, -53])
        self.move(2, [95, 0, -53])
        self.move(3, [95, 0, -53])
        self.move(4, [95, 0, -53])
        self.move(5, [95, 0, -53])
        self.move(6, [95, 0, -53])
        self.execute_move()
        time.sleep(1.2)
        self.move(1, [coord[0], 0, -10])
        self.move(2, [coord[0], 0, -10])
        self.move(3, [coord[0], 0, -10])
        self.move(4, [coord[0], 0, -10])
        self.move(5, [coord[0], 0, -10])
        self.move(6, [coord[0], 0, -10])
        self.execute_move()
        time.sleep(0.4)
        for i in range(-20, coord[2], -1):
            # print(i)
            self.move(1, [coord[0], 0, i])
            self.move(2, [coord[0], 0, i])
            self.move(3, [coord[0], 0, i])
            self.move(4, [coord[0], 0, i])
            self.move(5, [coord[0], 0, i])
            self.move(6, [coord[0], 0, i])
            self.execute_move()
            time.sleep(0.01)


    def draw(self):
        print(self.test_point)
        plot_3d_points(self.test_point)

    def reset(self):
        self.test_point = []


    def disable_force(self, ID):
        packet = [0xFF, 0xFF, ID, 0x04, 0x03, 0x28, 0]
        packet.append(self.calculate_checksum(packet[2:]))
        packet = bytearray(packet)
        self.ser.write(packet)




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

