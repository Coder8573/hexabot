import math
from distutils.command.config import config

import operations
import config


class Walk_Class:
    def __init__(self, origin_point):
        self.origin_point = origin_point
        self.walk_progress = [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0] # Range: 0 - 1
        #self.leg_states = ["Propelling", "Lifting", "Standing", "Reset"]
        self.leg_state = [0, 0, 0, 0, 0, 0]
        self.last_point = [[180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80]]
        #self.points = 0
        self.gait = 1

        self.push_fraction = 3/6
        self.speed_multiplier = 2
        self.lift_height_multiplier = 1.0
        self.max_step_length = 200

        self.test_points = []


    def gait_parameter(self, gait):
        if gait == 0:
            self.walk_progress[0] = 0
            self.walk_progress[1] = 0
            self.walk_progress[2] = 0
            self.walk_progress[3] = 0
            self.walk_progress[4] = 0
            self.walk_progress[5] = 0

            self.push_fraction = 3/6
            self.speed_multiplier = 0.8
            self.lift_height_multiplier = 1
            self.max_step_length = 240


        elif gait == 1:
            self.walk_progress[0] = 0
            self.walk_progress[1] = 1/2
            self.walk_progress[2] = 0
            self.walk_progress[3] = 1/2
            self.walk_progress[4] = 0
            self.walk_progress[5] = 1/2

            self.push_fraction = 3.1/6
            self.speed_multiplier = 1
            self.lift_height_multiplier = 1.1
            self.max_step_length = 240


        elif gait == 2:
            self.walk_progress[0] = 0
            self.walk_progress[1] = 1/6
            self.walk_progress[2] = 2/6
            self.walk_progress[3] = 5/6
            self.walk_progress[4] = 4/6
            self.walk_progress[5] = 3/6

            self.push_fraction = 5/6
            self.speed_multiplier = 1
            self.lift_height_multiplier = 1.3
            self.max_step_length = 150


    def gen_point(self, leg, joy1, joy2, gait, origin_point=None, last_point=None, last_points=None):
        self.gait_parameter(gait)
        if last_point:
            self.last_point[leg-1] = last_point
        if last_points:
            self.last_point = last_points
        if origin_point:
            self.origin_point = origin_point

        joy1hyp = operations.hypotenuse(joy1[0], joy1[1])
        joy2hyp = operations.hypotenuse(joy2[0], joy2[1])

        walk_speed = operations.map_value(operations.constrain(joy1hyp, 0, 1), 0.2, 1, 0, 1)
        stepsize = walk_speed * self.speed_multiplier

        #if math.sqrt(joy1[0] ** 2 + joy1[1] ** 2) > 0.2:
        if joy1[0] > 0:
            walk_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 90
        elif joy1[0] < 0:
            walk_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 270
        else:
            if joy1[1] >= 0:
                walk_dir = 180
            else:
                walk_dir = 0




        if joy2[0] < 0:
            turn_strength = operations.map_value(joy2[0], -1, 0, 0, -1)
            #turn_strength = (joy2[0]+0.2)/0.8
            #turn_strength = -(1 + turn_strength)
        else:
            turn_strength = operations.map_value(joy2[0], 0, 1, 1, 0)
            #turn_strength = (joy2[0]-0.2)/0.8
            #turn_strength = 1 - turn_strength

        #print(turn_strength)
        turn_strength = operations.constrain(turn_strength, -1, 1)
        #turn_strength = 0.4
        #print(turn_strength)
        turn_radius = (turn_strength*10)**5
        biggest_distance = 0
        for i in range(6):
            distance = math.sqrt((self.last_point[i][0] - (turn_radius * math.cos(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][i] + 180))))) ** 2 +
                                 (self.last_point[i][1] - (turn_radius * math.sin(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.cos(math.radians(config.data["legMountAngle"][i] + 180))))) ** 2)
            #print(f"new distance: {distance}")

            if distance > biggest_distance:
                biggest_distance = distance
        #print(biggest_distance)

        current_distance = math.sqrt((self.last_point[leg - 1][0] - (turn_radius * math.cos(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][leg - 1] + 180))))) ** 2 +
                                     (self.last_point[leg - 1][1] - (turn_radius * math.sin(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.cos(math.radians(config.data["legMountAngle"][leg - 1] + 180))))) ** 2)
        stepsize = stepsize * (current_distance/biggest_distance)
        #print(f"leg: {leg}, stepsize: {stepsize}")

        if (self.last_point[leg - 1][0] - turn_radius * math.cos(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][leg - 1] + 180)))) < 0:
            tangent_angle = math.degrees(math.atan(((self.last_point[leg - 1][1] - (turn_radius * math.sin(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.cos(math.radians(config.data["legMountAngle"][leg - 1] + 180))))) /
                                                    (self.last_point[leg - 1][0] - (turn_radius * math.cos(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][leg - 1] + 180))))))))
            #print(1)
        else:
            tangent_angle = math.degrees(math.atan(((self.last_point[leg - 1][1] - (turn_radius * math.sin(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.cos(math.radians(config.data["legMountAngle"][leg - 1] + 180))))) /
                                                    (self.last_point[leg - 1][0] - (turn_radius * math.cos(math.radians(walk_dir)) + ((self.origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][leg - 1] + 180)))))))) + 180
            #print(2)
        #print(tangent_angle)
        #print(f"tangent angle: {tangent_angle}")
        #print()
        #print([stepsize*math.cos(math.radians(tangent_angle+90)), stepsize*math.sin(math.radians(tangent_angle+90))])
        self.last_point[leg-1] = [self.last_point[leg - 1][0] + stepsize * math.cos(math.radians(tangent_angle + 90)), self.last_point[leg - 1][1] + stepsize * math.sin(math.radians(tangent_angle + 90)), self.last_point[leg - 1][2]]
        return self.last_point[leg-1]

