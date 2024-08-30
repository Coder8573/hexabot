import serial
import matplotlib.pyplot as plt

import kinematics
import walk


class Control:
    def __init__(self, port):
        self.walk_class = walk.WalkClass()
        self.port = port
        self.packet = []
        self.ser = serial.Serial(port, 1000000, timeout=1)
        self.calc = kinematics.calc()

        #print(self.calc.calc_steps_local_coord([180, 0, -120], 2))
        self.current_gait = 1
        self.new_gait = 1
        self.origin_point = [180, 0, -80]
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


    def calculate_checksum(self, data):
        checksum = sum(data) & 0xFF
        return (~checksum) & 0xFF

    def calc_low_byte(self, data):
        return data & 0xFF

    def calc_high_byte(self, data):
        return (data >> 8) & 0xFF


    def test_move(self, leg, coord, origin_point):
        print(self.calc.just_calc(coord, leg, origin_point), leg)
        #coord = self.calc.local_coord_to_abs_coord(coord, leg, self.origin_point)
        #self.test_point.append(coord)
        #print(f"Leg: {leg}, coord: {coord}")

    def move(self, leg, coord):
        steps = self.calc.calc_steps_abs_coord(coord, leg)
        packet = [0xFF, 0xFF, (leg*3)-2, 0x07, 0x03, 0x2A, self.calc_low_byte(steps[0]), self.calc_high_byte(steps[0])]
        packet.append(self.calculate_checksum(packet))
        self.ser.write(bytearray(packet))
        packet = [0xFF, 0xFF, (leg*3)-1, 0x07, 0x03, 0x2A, self.calc_low_byte(steps[1]), self.calc_high_byte(steps[1])]
        packet.append(self.calculate_checksum(packet))
        self.ser.write(bytearray(packet))
        packet = [0xFF, 0xFF, (leg*3), 0x07, 0x03, 0x2A, self.calc_low_byte(steps[2]), self.calc_high_byte(steps[2])]
        packet.append(self.calculate_checksum(packet))
        self.ser.write(bytearray(packet))

    def pre_move(self, leg, coord):  # , direction, speed, rotation
        steps = self.calc.calc_steps_abs_coord(coord, leg)
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
        self.last_points[leg-1] = coord

    def pre_move_local_coord(self, leg, coord, origin_point):  # , direction, speed, rotation
        print(coord)
        steps = self.calc.calc_steps_local_coord([coord[0] + origin_point[0], coord[1] + origin_point[1], coord[2] + origin_point[2]], leg)
        if not self.packet:
            self.packet = [0xFF, 0xFF, 0xFE, 27, 0x83, 0x2A, 0x06, (leg * 3) - 2, self.calc_low_byte(steps[0]),
                           self.calc_high_byte(steps[0]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3) - 1, self.calc_low_byte(steps[1]), self.calc_high_byte(steps[1]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3), self.calc_low_byte(steps[2]), self.calc_high_byte(steps[2]), 0X00, 0X00, 0x00, 0X00]
        else:
            self.packet.extend([
                (leg * 3) - 2, self.calc_low_byte(steps[0]), self.calc_high_byte(steps[0]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3) - 1, self.calc_low_byte(steps[1]), self.calc_high_byte(steps[1]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3), self.calc_low_byte(steps[2]), self.calc_high_byte(steps[2]), 0X00, 0X00, 0x00, 0X00])

    def just_move(self, leg, coord, origin_point):  # , direction, speed, rotation
        #print(coord)
        steps = self.calc.calc_steps_local_coord(self.calc.just_calc(coord, leg, origin_point), leg)
        print(self.calc.just_calc(coord, leg, origin_point), leg)
        if not self.packet:
            self.packet = [0xFF, 0xFF, 0xFE, 27, 0x83, 0x2A, 0x06, (leg * 3) - 2, self.calc_low_byte(steps[0]),
                           self.calc_high_byte(steps[0]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3) - 1, self.calc_low_byte(steps[1]), self.calc_high_byte(steps[1]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3), self.calc_low_byte(steps[2]), self.calc_high_byte(steps[2]), 0X00, 0X00, 0x00, 0X00]
        else:
            self.packet.extend([
                (leg * 3) - 2, self.calc_low_byte(steps[0]), self.calc_high_byte(steps[0]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3) - 1, self.calc_low_byte(steps[1]), self.calc_high_byte(steps[1]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3), self.calc_low_byte(steps[2]), self.calc_high_byte(steps[2]), 0X00, 0X00, 0x00, 0X00])

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

    def walk(self, walk_dir, walk_speed, turn_vector, gait):
        #print(f"Walk dir: {walk_dir}, speed: {walk_speed}, trun vector: {turn_vector}, gait: {gait}")
        self.new_gait = gait
        if self.current_gait != self.new_gait:
            # needs to home
            self.current_gait = self.new_gait
            for i in range(6):
                self.last_points[i] = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        #print(f"old: {self.last_points}")
        self.new_points = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.new_points[0] = self.walk_class.gen_point(1, walk_dir, walk_speed, turn_vector, gait, self.last_points, self.origin_point)
        self.new_points[1] = self.walk_class.gen_point(2, walk_dir, walk_speed, turn_vector, gait, self.last_points, self.origin_point)
        self.new_points[2] = self.walk_class.gen_point(3, walk_dir, walk_speed, turn_vector, gait, self.last_points, self.origin_point)
        self.new_points[3] = self.walk_class.gen_point(4, walk_dir, walk_speed, turn_vector, gait, self.last_points, self.origin_point)
        self.new_points[4] = self.walk_class.gen_point(5, walk_dir, walk_speed, turn_vector, gait, self.last_points, self.origin_point)
        self.new_points[5] = self.walk_class.gen_point(6, walk_dir, walk_speed, turn_vector, gait, self.last_points, self.origin_point)
        self.last_points = self.new_points
        #for i in range(6):
        #    self.new_points[i] = [self.last_points[i][0] + self.origin_point[0], self.last_points[i][1] + self.origin_point[1], self.last_points[i][2] + self.origin_point[2]]
        self.just_move(1, self.new_points[0], self.origin_point)
        self.just_move(2, self.new_points[1], self.origin_point)
        self.just_move(3, self.new_points[2], self.origin_point)
        self.just_move(4, self.new_points[3], self.origin_point)
        self.just_move(5, self.new_points[4], self.origin_point)
        self.just_move(6, self.new_points[5], self.origin_point)
        self.execute_move()
        #print(self.new_points)
        #print(self.last_points)

    def draw(self):
        print(self.test_point)
        plot_3d_points(self.test_point)

    def reset(self):
        self.test_point = []
        self.last_points = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.new_points = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

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

