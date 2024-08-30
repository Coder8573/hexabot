import time
import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import kinematics
import walk

class control():
    def __init__(self, port):
        self.port = port
        self.packet = []
        self.ser = serial.Serial(port, 1000000, timeout=1)
        self.calc = kinematics.calc()
        self.walk_points = []
        self.next_point = 0
        self.walk_points = walk.gen_foot_path()
        self.last_points = [[], [], [], [], [], []]

    def close(self):
        self.ser.close()

    def calculate_checksum(self, data):
        checksum = sum(data) & 0xFF
        return (~checksum) & 0xFF

    def calc_low_byte(self, data):
        return data & 0xFF

    def calc_high_byte(self, data):
        return (data >> 8) & 0xFF

    def move(self, leg, coord):
        steps = self.calc.calc_steps(coord, leg)
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
        steps = self.calc.calc_steps(coord, leg)
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


    def pre_move_local_coord(self, leg, coord):  # , direction, speed, rotation
        steps = self.calc.calc_steps_local_coord(coord, leg)
        if not self.packet:
            self.packet = [0xFF, 0xFF, 0xFE, 27, 0x83, 0x2A, 0x06, (leg*3)-2, self.calc_low_byte(steps[0]), self.calc_high_byte(steps[0]), 0X00, 0X00, 0x00, 0X00
                      , (leg*3)-1, self.calc_low_byte(steps[1]), self.calc_high_byte(steps[1]), 0X00, 0X00, 0x00, 0X00
                      , (leg*3), self.calc_low_byte(steps[2]), self.calc_high_byte(steps[2]), 0X00, 0X00, 0x00, 0X00]
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

    def walk(self, dir, speed, method=1):
        if method == 1:
             if self.next_point >= len(self.walk_points):
                 self.next_point = 0

             self.pre_move(2, walk.gen_next_point(2, dir, [160, 0, -160], self.next_point, self.walk_points))
             self.pre_move(4, walk.gen_next_point(4, dir, [160, 0, -160], self.next_point, self.walk_points))
             self.pre_move(6, walk.gen_next_point(6, dir, [160, 0, -160], self.next_point, self.walk_points))

             if self.next_point + len(self.walk_points)/2 <= len(self.walk_points):
                self.pre_move(1, walk.gen_next_point(1, dir, [160, 0, -160], self.next_point + int(round(0.5*len(self.walk_points), 0))-1, self.walk_points))
                self.pre_move(3, walk.gen_next_point(3, dir, [160, 0, -160], self.next_point + int(round(0.5*len(self.walk_points), 0))-1, self.walk_points))
                self.pre_move(5, walk.gen_next_point(5, dir, [160, 0, -160], self.next_point + int(round(0.5*len(self.walk_points), 0))-1, self.walk_points))
                #self.next_point = self.next_point + 1
             else:
                self.pre_move(1, walk.gen_next_point(1, dir, [160, 0, -160], self.next_point - int(round(0.5*len(self.walk_points), 0)), self.walk_points))
                self.pre_move(3, walk.gen_next_point(3, dir, [160, 0, -160], self.next_point - int(round(0.5*len(self.walk_points), 0)), self.walk_points))
                self.pre_move(5, walk.gen_next_point(5, dir, [160, 0, -160], self.next_point - int(round(0.5*len(self.walk_points), 0)), self.walk_points))
             self.execute_move()
             self.next_point = self.next_point + 1


        elif method == 2:
            if self.next_point >= len(self.walk_points):
                self.next_point = 0
            self.pre_move(1, walk.gen_next_point(1, dir, [160, 0, -160], self.next_point, self.walk_points))
            self.pre_move(4, walk.gen_next_point(4, dir, [160, 0, -160], self.next_point, self.walk_points))
            if self.next_point + len(self.walk_points)/3 <= len(self.walk_points):
               self.pre_move(2, walk.gen_next_point(2, dir, [160, 0, -160], self.next_point + int(round(len(self.walk_points)/3, 0))-1, self.walk_points))
               self.pre_move(5, walk.gen_next_point(5, dir, [160, 0, -160], self.next_point + int(round(len(self.walk_points)/3, 0))-1, self.walk_points))
            else:
               self.pre_move(2, walk.gen_next_point(2, dir, [160, 0, -160], self.next_point - int(round((len(self.walk_points)/3)*2, 0)), self.walk_points))
               self.pre_move(5, walk.gen_next_point(5, dir, [160, 0, -160], self.next_point - int(round((len(self.walk_points)/3)*2, 0)), self.walk_points))


            if self.next_point + (len(self.walk_points)/3)*2 <= len(self.walk_points):
               self.pre_move(3, walk.gen_next_point(3, dir, [160, 0, -160], self.next_point + int(round((len(self.walk_points)/3)*2, 0))-1, self.walk_points))
               self.pre_move(6, walk.gen_next_point(6, dir, [160, 0, -160], self.next_point + int(round((len(self.walk_points)/3)*2, 0))-1, self.walk_points))
            else:
               self.pre_move(3, walk.gen_next_point(3, dir, [160, 0, -160], self.next_point - int(round(len(self.walk_points)/3, 0)), self.walk_points))
               self.pre_move(6, walk.gen_next_point(6, dir, [160, 0, -160], self.next_point - int(round(len(self.walk_points)/3, 0)), self.walk_points))

            self.execute_move()
            self.next_point = self.next_point + 1

    def walk_to_home_pos(self):
        if self.next_point >= len(self.walk_points):
            self.next_point = 0
        self.pre_move(2, walk.gen_next_point(2, dir, [160, 0, -160], self.next_point, self.walk_points))
        self.pre_move(4, walk.gen_next_point(4, dir, [160, 0, -160], self.next_point, self.walk_points))
        self.pre_move(6, walk.gen_next_point(6, dir, [160, 0, -160], self.next_point, self.walk_points))
        if self.next_point + len(self.walk_points)/2 <= len(self.walk_points):
           self.pre_move(1, walk.gen_next_point(1, dir, [160, 0, -160], self.next_point + int(round(0.5*len(self.walk_points), 0))-1, self.walk_points))
           self.pre_move(3, walk.gen_next_point(3, dir, [160, 0, -160], self.next_point + int(round(0.5*len(self.walk_points), 0))-1, self.walk_points))
           self.pre_move(5, walk.gen_next_point(5, dir, [160, 0, -160], self.next_point + int(round(0.5*len(self.walk_points), 0))-1, self.walk_points))
           #self.next_point = self.next_point + 1
        else:
           self.pre_move(1, walk.gen_next_point(1, dir, [160, 0, -160], self.next_point - int(round(0.5*len(self.walk_points), 0)), self.walk_points))
           self.pre_move(3, walk.gen_next_point(3, dir, [160, 0, -160], self.next_point - int(round(0.5*len(self.walk_points), 0)), self.walk_points))
           self.pre_move(5, walk.gen_next_point(5, dir, [160, 0, -160], self.next_point - int(round(0.5*len(self.walk_points), 0)), self.walk_points))
        self.execute_move()
        self.next_point = self.next_point + 1




    def plot_walk(self):
        self.next_point = 0
        gen_points = []
        if not self.walk_points or self.next_point >= len(self.walk_points):
            self.next_point = 0
        for dir in range(180, 360, 90):
            for i in range(0, len(self.walk_points)):
                if not self.walk_points or self.next_point >= len(self.walk_points):
                    self.walk_points = walk.gen_foot_path()
                    self.next_point = 0
                # print(i)
                gen_points.append(walk.gen_next_point(1, dir, [160, 0, -160], self.next_point, self.walk_points))
                gen_points.append(walk.gen_next_point(2, dir, [160, 0, -160], self.next_point, self.walk_points))
                gen_points.append(walk.gen_next_point(3, dir, [160, 0, -160], self.next_point, self.walk_points))
                gen_points.append(walk.gen_next_point(4, dir, [160, 0, -160], self.next_point, self.walk_points))
                gen_points.append(walk.gen_next_point(5, dir, [160, 0, -160], self.next_point, self.walk_points))
                gen_points.append(walk.gen_next_point(6, dir, [160, 0, -160], self.next_point, self.walk_points))
                gen_points.append(self.calc.calc_local_coords(walk.gen_next_point(1, dir, [160, 0, -160], self.next_point, self.walk_points), 1))
                gen_points.append(self.calc.calc_local_coords(walk.gen_next_point(2, dir, [160, 0, -160], self.next_point, self.walk_points), 2))
                gen_points.append(self.calc.calc_local_coords(walk.gen_next_point(3, dir, [160, 0, -160], self.next_point, self.walk_points), 3))
                gen_points.append(self.calc.calc_local_coords(walk.gen_next_point(4, dir, [160, 0, -160], self.next_point, self.walk_points), 4))
                gen_points.append(self.calc.calc_local_coords(walk.gen_next_point(5, dir, [160, 0, -160], self.next_point, self.walk_points), 5))
                gen_points.append(self.calc.calc_local_coords(walk.gen_next_point(6, dir, [160, 0, -160], self.next_point, self.walk_points), 6))
                self.next_point = self.next_point + 1
        plot_3d_points(gen_points)

    def disable_force(self, ID):
        packet = [0xFF, 0xFF, ID, 0x04, 0x03, 0x28, 0]
        packet.append(self.calculate_checksum(packet[2:]))
        packet = bytearray(packet)
        self.ser.write(packet)

    def home(self, coord=(150, 0, -160)):
        pass
        self.pre_move_local_coord(1, [80, 0, -30])
        self.pre_move_local_coord(2, [80, 0, -30])
        self.pre_move_local_coord(3, [80, 0, -30])
        self.pre_move_local_coord(4, [80, 0, -30])
        self.pre_move_local_coord(5, [80, 0, -30])
        self.pre_move_local_coord(6, [80, 0, -30])
        self.execute_move()
        time.sleep(0.8)
        self.pre_move_local_coord(1, [coord[0], 0, -10])
        self.pre_move_local_coord(2, [coord[0], 0, -10])
        self.pre_move_local_coord(3, [coord[0], 0, -10])
        self.pre_move_local_coord(4, [coord[0], 0, -10])
        self.pre_move_local_coord(5, [coord[0], 0, -10])
        self.pre_move_local_coord(6, [coord[0], 0, -10])
        self.execute_move()
        time.sleep(0.2)
        for i in range(-20, coord[2], -1):
            # print(i)
            self.pre_move_local_coord(1, [coord[0], 0, i])
            self.pre_move_local_coord(2, [coord[0], 0, i])
            self.pre_move_local_coord(3, [coord[0], 0, i])
            self.pre_move_local_coord(4, [coord[0], 0, i])
            self.pre_move_local_coord(5, [coord[0], 0, i])
            self.pre_move_local_coord(6, [coord[0], 0, i])
            self.execute_move()
            time.sleep(0.01)

    def read_pos(self):
        packet = [255, 255, 254, 0, 0x82, 0x38, 0x08]
        for i in range(0, 2):
            packet.append(i+1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet)-2)
        print(packet)
        self.ser.write(bytearray(packet))
        time.sleep(0.5)
        packet = []
        while self.ser.in_waiting:
            while not self.ser.in_waiting:
                pass
            packet.append(hex(int.from_bytes(self.ser.read(), "little")))
            #packet.append(self.ser.read())
        print(f"read packet: {packet}")


    def read_speed(self):
        pass

    def read_load(self):
        pass

    def read_voltage(self):
        pass

    def read_current(self):
        pass

    def read_temperature(self):
        pass

    def read_is_moving(self):
        pass





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


