import time
import serial
import matplotlib.pyplot as plt

import kinematics
import walk

class control():
    def __init__(self, port):
        self.port = port
        self.packet = []
        self.ser = serial.Serial(port, 1000000, timeout=1)
        self.calc = kinematics.calc()
        self.path_point = [0, 0, 0]
        self.point = [[], [], [], [], [], []]
        self.walk_progress = 0
        self.current_gait = 1
        self.new_gait = 1
        self.last_dir = 0

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

    def turn(self, turn_dir, turn_strength, origin_point):
        stepsize = (turn_strength - 0.20) * 0.8 + 0.05
        ground_touching_percentage = 50

        self.walk_progress = walk.gen_next_point(0, self.walk_progress, stepsize, 1, turn_dir, 0, ground_touching_percentage, origin_point)
        self.pre_move_local_coord(1, walk.gen_next_point(1, self.walk_progress + 50, stepsize, 1, turn_dir, 0, ground_touching_percentage, origin_point))
        self.pre_move_local_coord(2, walk.gen_next_point(2, self.walk_progress, stepsize, 1, turn_dir, 0, ground_touching_percentage, origin_point))
        self.pre_move_local_coord(3, walk.gen_next_point(3, self.walk_progress + 50, stepsize, 1, turn_dir, 0, ground_touching_percentage, origin_point))
        self.pre_move_local_coord(4, walk.gen_next_point(4, self.walk_progress, stepsize, 1, turn_dir, 0, ground_touching_percentage, origin_point))
        self.pre_move_local_coord(5, walk.gen_next_point(5, self.walk_progress + 50, stepsize, 1, turn_dir, 0, ground_touching_percentage, origin_point))
        self.pre_move_local_coord(6, walk.gen_next_point(6, self.walk_progress, stepsize, 1, turn_dir, 0, ground_touching_percentage, origin_point))
        self.execute_move()



    def walk(self, dir, speed, turn_strength, turn_dir, gait=1, origin_point=(180, 0, -80)):
        self.new_gait = gait
        self.last_dir = dir
        if self.current_gait != self.new_gait:
            #self.walk_to_home_pos()
            self.current_gait = self.new_gait

        if self.current_gait == 0:  # Monogait
            stepsize = (speed-0.20)*0.5+0.05
            ground_touching_percentage = 50
            self.path_point, self.walk_progress = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)
            self.point[0] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[1] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[2] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[3] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[4] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[5] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.pre_move_local_coord(1, walk.path_point_to_local_coord(1, self.point[0], orgin_point, dir))
            self.pre_move_local_coord(2, walk.path_point_to_local_coord(2, self.point[1], orgin_point, dir))
            self.pre_move_local_coord(3, walk.path_point_to_local_coord(3, self.point[2], orgin_point, dir))
            self.pre_move_local_coord(4, walk.path_point_to_local_coord(4, self.point[3], orgin_point, dir))
            self.pre_move_local_coord(5, walk.path_point_to_local_coord(5, self.point[4], orgin_point, dir))
            self.pre_move_local_coord(6, walk.path_point_to_local_coord(6, self.point[5], orgin_point, dir))
            self.execute_move()

        if self.current_gait == 1:  # Trigait
            stepsize = (speed-0.20)*0.8+0.05
            ground_touching_percentage = 50
            self.walk_progress = walk.gen_next_point(0, self.walk_progress, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point)
            self.pre_move_local_coord(1, walk.gen_next_point(1, self.walk_progress + 50, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            self.pre_move_local_coord(2, walk.gen_next_point(2, self.walk_progress, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            self.pre_move_local_coord(3, walk.gen_next_point(3, self.walk_progress + 50, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            self.pre_move_local_coord(4, walk.gen_next_point(4, self.walk_progress, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            self.pre_move_local_coord(5, walk.gen_next_point(5, self.walk_progress + 50, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            self.pre_move_local_coord(6, walk.gen_next_point(6, self.walk_progress, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            self.execute_move()


            #points = []
            #for i in range(int(round(100/stepsize, 0))):
            #    self.walk_progress = walk.gen_next_point(0, self.walk_progress, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point)
            #    points.append(walk.gen_next_point(1, self.walk_progress+50, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            #    points.append(walk.gen_next_point(2, self.walk_progress, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            #    points.append(walk.gen_next_point(3, self.walk_progress+50, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            #    points.append(walk.gen_next_point(4, self.walk_progress, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            #    points.append(walk.gen_next_point(5, self.walk_progress+50, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            #    points.append(walk.gen_next_point(6, self.walk_progress, stepsize, turn_strength, turn_dir, dir, ground_touching_percentage, origin_point))
            #plot_3d_points(points)
            #self.pre_move_local_coord(1, walk.path_point_to_local_coord(1, self.point[0], orgin_point, dir))
            #self.pre_move_local_coord(2, walk.path_point_to_local_coord(2, self.point[1], orgin_point, dir))
            #self.pre_move_local_coord(3, walk.path_point_to_local_coord(3, self.point[2], orgin_point, dir))
            #self.pre_move_local_coord(4, walk.path_point_to_local_coord(4, self.point[3], orgin_point, dir))
            #self.pre_move_local_coord(5, walk.path_point_to_local_coord(5, self.point[4], orgin_point, dir))
            #self.pre_move_local_coord(6, walk.path_point_to_local_coord(6, self.point[5], orgin_point, dir))
            #self.execute_move()

        elif self.current_gait == 2:  # Wavegait
            stepsize = (speed - 0.20) * 0.3 + 0.05
            ground_touching_percentage = 84
            self.path_point, self.walk_progress = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)
            self.point[0] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[1] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 1, ground_touching_percentage)[0]
            self.point[2] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 2, ground_touching_percentage)[0]
            self.point[3] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 3, ground_touching_percentage)[0]
            self.point[4] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 4, ground_touching_percentage)[0]
            self.point[5] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 5, ground_touching_percentage)[0]
            self.pre_move_local_coord(1, walk.path_point_to_local_coord(1, self.point[0], orgin_point, dir))
            self.pre_move_local_coord(2, walk.path_point_to_local_coord(2, self.point[1], orgin_point, dir))
            self.pre_move_local_coord(3, walk.path_point_to_local_coord(3, self.point[2], orgin_point, dir))
            self.pre_move_local_coord(4, walk.path_point_to_local_coord(4, self.point[3], orgin_point, dir))
            self.pre_move_local_coord(5, walk.path_point_to_local_coord(5, self.point[4], orgin_point, dir))
            self.pre_move_local_coord(6, walk.path_point_to_local_coord(6, self.point[5], orgin_point, dir))
            self.execute_move()

        elif self.current_gait == 3:  # Ripplegait
            stepsize = (speed - 0.20) * 0.8 + 0.05
            ground_touching_percentage = 53
            self.path_point, self.walk_progress = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)
            self.point[0] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[1] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 4, ground_touching_percentage)[0]
            self.point[2] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 2, ground_touching_percentage)[0]
            self.point[3] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 5, ground_touching_percentage)[0]
            self.point[4] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6), ground_touching_percentage)[0]
            self.point[5] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 6) * 3, ground_touching_percentage)[0]
            self.pre_move_local_coord(1, walk.path_point_to_local_coord(1, self.point[0], orgin_point, dir))
            self.pre_move_local_coord(2, walk.path_point_to_local_coord(2, self.point[1], orgin_point, dir))
            self.pre_move_local_coord(3, walk.path_point_to_local_coord(3, self.point[2], orgin_point, dir))
            self.pre_move_local_coord(4, walk.path_point_to_local_coord(4, self.point[3], orgin_point, dir))
            self.pre_move_local_coord(5, walk.path_point_to_local_coord(5, self.point[4], orgin_point, dir))
            self.pre_move_local_coord(6, walk.path_point_to_local_coord(6, self.point[5], orgin_point, dir))
            self.execute_move()

        elif self.current_gait == 4:  # Bigait
            stepsize = (speed - 0.20) * 0.8 + 0.05
            ground_touching_percentage = 35
            self.path_point, self.walk_progress = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)
            self.point[0] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[1] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 3), ground_touching_percentage)[0]
            self.point[2] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 3) * 2, ground_touching_percentage)[0]
            self.point[3] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[4] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 3), ground_touching_percentage)[0]
            self.point[5] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 3) * 2, ground_touching_percentage)[0]
            self.pre_move_local_coord(1, walk.path_point_to_local_coord(1, self.point[0], orgin_point, dir))
            self.pre_move_local_coord(2, walk.path_point_to_local_coord(2, self.point[1], orgin_point, dir))
            self.pre_move_local_coord(3, walk.path_point_to_local_coord(3, self.point[2], orgin_point, dir))
            self.pre_move_local_coord(4, walk.path_point_to_local_coord(4, self.point[3], orgin_point, dir))
            self.pre_move_local_coord(5, walk.path_point_to_local_coord(5, self.point[4], orgin_point, dir))
            self.pre_move_local_coord(6, walk.path_point_to_local_coord(6, self.point[5], orgin_point, dir))
            self.execute_move()

        elif self.current_gait == 5:  # Quadgait
            stepsize = (speed - 0.20) * 0.5 + 0.05
            ground_touching_percentage = 68
            self.path_point, self.walk_progress = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)
            self.point[0] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[1] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 3), ground_touching_percentage)[0]
            self.point[2] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 3) * 2, ground_touching_percentage)[0]
            self.point[3] = walk.gen_next_path_point(stepsize, self.walk_progress, ground_touching_percentage)[0]
            self.point[4] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 3), ground_touching_percentage)[0]
            self.point[5] = walk.gen_next_path_point(stepsize, self.walk_progress + (100 / 3) * 2, ground_touching_percentage)[0]
            self.pre_move_local_coord(1, walk.path_point_to_local_coord(1, self.point[0], orgin_point, dir))
            self.pre_move_local_coord(2, walk.path_point_to_local_coord(2, self.point[1], orgin_point, dir))
            self.pre_move_local_coord(3, walk.path_point_to_local_coord(3, self.point[2], orgin_point, dir))
            self.pre_move_local_coord(4, walk.path_point_to_local_coord(4, self.point[3], orgin_point, dir))
            self.pre_move_local_coord(5, walk.path_point_to_local_coord(5, self.point[4], orgin_point, dir))
            self.pre_move_local_coord(6, walk.path_point_to_local_coord(6, self.point[5], orgin_point, dir))
            self.execute_move()

    def walk_to_home_pos(self):
        if self.current_gait == 1:  # Trigait
            stepsize = 1
            end_point = (180, 0, -120)
            orgin_point = (180, 0, -80)
            points = []
            points2 = []
            dir = self.last_dir
            #if walk.diff_between_two_points(self.point[0], (180, 0, -100)) < walk.diff_between_two_points(self.point[1], (180, 0, -100)):
            #    for t in range(0, 101):
            #        points.append(walk.gen_home_curve_point(1, t, dir, self.point[0], end_point=end_point))
            #        points.append(walk.gen_home_curve_point(3, t, dir, self.point[2], end_point=end_point))
            #        points.append(walk.gen_home_curve_point(5, t, dir, self.point[4], end_point=end_point))
#
            #    for t in range(0, 101):
            #        points2.append(walk.gen_home_curve_point(2, t, dir, self.point[1], end_point=end_point))
            #        points2.append(walk.gen_home_curve_point(4, t, dir, self.point[3], end_point=end_point))
            #        points2.append(walk.gen_home_curve_point(6, t, dir, self.point[5], end_point=end_point))
#
            #else:
            #    for t in range(0, 101):
            #        points.append(walk.gen_home_curve_point(2, t, dir, self.point[1], end_point=end_point))
            #        points.append(walk.gen_home_curve_point(4, t, dir, self.point[3], end_point=end_point))
            #        points.append(walk.gen_home_curve_point(6, t, dir, self.point[5], end_point=end_point))
#
            #    for t in range(0, 101):
            #        points2.append(walk.gen_home_curve_point(1, t, dir, self.point[0], end_point=end_point))
            #        points2.append(walk.gen_home_curve_point(3, t, dir, self.point[2], end_point=end_point))
            #        points2.append(walk.gen_home_curve_point(5, t, dir, self.point[4], end_point=end_point))
#
            #plot_3d_points(points)
            #plot_3d_points(points2)
            #points.extend(points2)
            #plot_3d_points(points)


            if walk.diff_between_two_points(self.point[0], (180, 0, -100)) < walk.diff_between_two_points(self.point[1], (180, 0, -100)):
                for t in range(0, 101):
                    self.pre_move_local_coord(1, walk.gen_home_curve_point(1, t, dir, self.point[0], end_point=end_point))
                    self.pre_move_local_coord(3, walk.gen_home_curve_point(3, t, dir, self.point[2], end_point=end_point))
                    self.pre_move_local_coord(5, walk.gen_home_curve_point(5, t, dir, self.point[4], end_point=end_point))

                    self.pre_move_local_coord(2, walk.path_point_to_local_coord(2, self.point[1], orgin_point, dir))
                    self.pre_move_local_coord(4, walk.path_point_to_local_coord(4, self.point[3], orgin_point, dir))
                    self.pre_move_local_coord(6, walk.path_point_to_local_coord(6, self.point[5], orgin_point, dir))
                    self.execute_move()
                    time.sleep(0.005)
                for t in range(0, 101):
                    self.pre_move_local_coord(2, walk.gen_home_curve_point(2, t, dir, self.point[1], end_point=end_point))
                    self.pre_move_local_coord(4, walk.gen_home_curve_point(4, t, dir, self.point[3], end_point=end_point))
                    self.pre_move_local_coord(6, walk.gen_home_curve_point(6, t, dir, self.point[5], end_point=end_point))

                    self.pre_move_local_coord(1, walk.gen_home_curve_point(1, 100, dir, self.point[0], end_point=end_point))
                    self.pre_move_local_coord(3, walk.gen_home_curve_point(3, 100, dir, self.point[2], end_point=end_point))
                    self.pre_move_local_coord(5, walk.gen_home_curve_point(5, 100, dir, self.point[4], end_point=end_point))
                    self.execute_move()
                    time.sleep(0.005)
            else:
                for t in range(0, 101):
                    self.pre_move_local_coord(2, walk.gen_home_curve_point(2, t, dir, self.point[1], end_point=end_point))
                    self.pre_move_local_coord(4, walk.gen_home_curve_point(4, t, dir, self.point[3], end_point=end_point))
                    self.pre_move_local_coord(6, walk.gen_home_curve_point(6, t, dir, self.point[5], end_point=end_point))

                    self.pre_move_local_coord(1, walk.path_point_to_local_coord(1, self.point[0], orgin_point, dir))
                    self.pre_move_local_coord(3, walk.path_point_to_local_coord(3, self.point[2], orgin_point, dir))
                    self.pre_move_local_coord(5, walk.path_point_to_local_coord(5, self.point[4], orgin_point, dir))
                    self.execute_move()
                    time.sleep(0.005)
                for t in range(0, 101):
                    self.pre_move_local_coord(1, walk.gen_home_curve_point(1, t, dir, self.point[0], end_point=end_point))
                    self.pre_move_local_coord(3, walk.gen_home_curve_point(3, t, dir, self.point[2], end_point=end_point))
                    self.pre_move_local_coord(5, walk.gen_home_curve_point(5, t, dir, self.point[4], end_point=end_point))

                    self.pre_move_local_coord(2, walk.gen_home_curve_point(2, 100, dir, self.point[1], end_point=end_point))
                    self.pre_move_local_coord(4, walk.gen_home_curve_point(4, 100, dir, self.point[3], end_point=end_point))
                    self.pre_move_local_coord(6, walk.gen_home_curve_point(6, 100, dir, self.point[5], end_point=end_point))
                    self.execute_move()
                    time.sleep(0.005)



            #print(points)
            #plot_3d_points(points)




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
                gen_points.append(self.calc.calc_local_coords(
                    walk.gen_next_point(1, dir, [160, 0, -160], self.next_point, self.walk_points), 1))
                gen_points.append(self.calc.calc_local_coords(
                    walk.gen_next_point(2, dir, [160, 0, -160], self.next_point, self.walk_points), 2))
                gen_points.append(self.calc.calc_local_coords(
                    walk.gen_next_point(3, dir, [160, 0, -160], self.next_point, self.walk_points), 3))
                gen_points.append(self.calc.calc_local_coords(
                    walk.gen_next_point(4, dir, [160, 0, -160], self.next_point, self.walk_points), 4))
                gen_points.append(self.calc.calc_local_coords(
                    walk.gen_next_point(5, dir, [160, 0, -160], self.next_point, self.walk_points), 5))
                gen_points.append(self.calc.calc_local_coords(
                    walk.gen_next_point(6, dir, [160, 0, -160], self.next_point, self.walk_points), 6))
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
        for point_num in range(6):
            self.point[point_num] = coord
        self.walk_progress = 0

    def read_all(self):
        packet = [255, 255, 254, 0, 0x82, 0x38, 0x08]
        for i in range(0, 4):
            packet.append(i + 1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet) - 2)
        print(packet)
        self.ser.write(bytearray(packet))
        packet = []
        while not self.ser.in_waiting:
            pass
        while self.ser.in_waiting:
            packet.append(int.from_bytes(self.ser.read(), "little"))
            time.sleep(0.0000000001)
        new_packets = []
        for i in range(int(len(packet) / (packet[3] + 4))):
            new_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
        print(f"read packet: {packet}")
        print(new_packets)
        # for i in new_packets:
        #    print(f"""Motor{i[2]} is {((i[4]-1)*-1)*"not"} running with speed: {0}""")

    def read_pos(self):
        packet = [255, 255, 254, 0, 0x82, 0x38, 0x02]
        for i in range(0, 18):
            packet.append(i + 1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet) - 2)
        self.ser.write(bytearray(packet))
        packet = []
        while not self.ser.in_waiting:
            pass
        while self.ser.in_waiting:
            packet.append(int.from_bytes(self.ser.read(), "little"))
            time.sleep(0.0000000001)
        seperate_motor_packets = []
        return_package = []
        for i in range(int(len(packet) / (packet[3] + 4))):
            seperate_motor_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
        for motor_packet in seperate_motor_packets:
            print(
                f"""{motor_packet}; pos: {motor_packet[5] + motor_packet[6] * 256}steps; {(motor_packet[5] + motor_packet[6] * 256) * (45 / 512)}deg """)
            return_package.append((motor_packet[5] + motor_packet[6] * 256) * (45 / 512))
        return return_package

    def read_speed(self):
        packet = [255, 255, 254, 0, 0x82, 0x3A, 0x02]
        for i in range(0, 18):
            packet.append(i + 1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet) - 2)
        self.ser.write(bytearray(packet))
        packet = []
        while not self.ser.in_waiting:
            pass
        while self.ser.in_waiting:
            packet.append(int.from_bytes(self.ser.read(), "little"))
            time.sleep(0.0000000001)
        seperate_motor_packets = []
        return_package = []
        for i in range(int(len(packet) / (packet[3] + 4))):
            seperate_motor_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
        for motor_packet in seperate_motor_packets:
            print(f"""{motor_packet}; speed: {motor_packet[5] + motor_packet[6] * 256}steps/s""")
            return_package.append(motor_packet[5] + motor_packet[6] * 256)
        return return_package

    def read_load(self):
        packet = [255, 255, 254, 0, 0x82, 0x3c, 0x01]
        for i in range(0, 18):
            packet.append(i + 1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet) - 2)
        self.ser.write(bytearray(packet))
        packet = []
        while not self.ser.in_waiting:
            pass
        while self.ser.in_waiting:
            packet.append(int.from_bytes(self.ser.read(), "little"))
            time.sleep(0.0000000001)
        seperate_motor_packets = []
        return_package = []
        for i in range(int(len(packet) / (packet[3] + 4))):
            seperate_motor_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
        print(packet)
        for motor_packet in seperate_motor_packets:
            print(f"""{motor_packet}; load: {motor_packet[5] / 10}%""")
            return_package.append(motor_packet[5] / 10)
        return return_package

    def read_voltage(self):
        packet = [255, 255, 254, 0, 0x82, 0x3e, 0x01]
        for i in range(0, 18):
            packet.append(i + 1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet) - 2)
        self.ser.write(bytearray(packet))
        packet = []
        while not self.ser.in_waiting:
            pass
        while self.ser.in_waiting:
            packet.append(int.from_bytes(self.ser.read(), "little"))
            time.sleep(0.0000000001)
        seperate_motor_packets = []
        return_package = []
        for i in range(int(len(packet) / (packet[3] + 4))):
            seperate_motor_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
        print(packet)
        for motor_packet in seperate_motor_packets:
            print(f"""{motor_packet}; voltage: {motor_packet[5] / 10}V""")
            return_package.append(motor_packet[5] / 10)
        return return_package

    def read_current(self):
        packet = [255, 255, 254, 0, 0x82, 0x45, 0x02]
        for i in range(0, 18):
            packet.append(i + 1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet) - 2)
        self.ser.write(bytearray(packet))
        packet = []
        while not self.ser.in_waiting:
            pass
        while self.ser.in_waiting:
            packet.append(int.from_bytes(self.ser.read(), "little"))
            time.sleep(0.0000000001)
        seperate_motor_packets = []
        return_package = []
        for i in range(int(len(packet) / (packet[3] + 4))):
            seperate_motor_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
        for motor_packet in seperate_motor_packets:
            print(f"""{motor_packet}; current: {(motor_packet[5] + motor_packet[6] * 256) * 6.5}mA""")
            return_package.append((motor_packet[5] + motor_packet[6] * 256) * 6.5)
        return return_package

    def read_temperature(self):
        packet = [255, 255, 254, 0, 0x82, 0x3f, 0x01]
        for i in range(0, 18):
            packet.append(i + 1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet) - 2)
        self.ser.write(bytearray(packet))
        packet = []
        while not self.ser.in_waiting:
            pass
        while self.ser.in_waiting:
            packet.append(int.from_bytes(self.ser.read(), "little"))
            time.sleep(0.0000000001)
        seperate_motor_packets = []
        return_package = []
        for i in range(int(len(packet) / (packet[3] + 4))):
            seperate_motor_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
        print(packet)
        for motor_packet in seperate_motor_packets:
            print(f"""{motor_packet}; temp: {motor_packet[5]}°C""")
            return_package.append(motor_packet[5])
        return return_package

    def read_is_moving(self):
        packet = [255, 255, 254, 0, 0x82, 0x42, 0x01]
        for i in range(0, 18):
            packet.append(i + 1)
        packet[3] = len(packet[3:])
        packet.append(self.calculate_checksum(packet) - 2)
        self.ser.write(bytearray(packet))
        packet = []
        while not self.ser.in_waiting:
            pass
        while self.ser.in_waiting:
            packet.append(int.from_bytes(self.ser.read(), "little"))
            time.sleep(0.0000000001)
        seperate_motor_packets = []
        return_package = []
        for i in range(int(len(packet) / (packet[3] + 4))):
            seperate_motor_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
        print(packet)
        for motor_packet in seperate_motor_packets:
            print(f"""{motor_packet}; moving: {motor_packet[5]}""")
            return_package.append(motor_packet[5])
        return return_package



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


