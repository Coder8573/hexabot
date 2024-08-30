import math
from distutils.command.config import config

import operations
import config


class WalkClass:
    def __init__(self):
        self.walk_progress = [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0] # Range: 0 - 1
        self.leg_states = ["Propelling", "Lifting", "Standing", "Reset"]
        self.leg_state = [0, 0, 0, 0, 0, 0]
        self.points = 0
        self.gait = 1

        self.push_fraction = 3/6
        self.speed_multiplier = 0.5
        self.max_speed = 100

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


        elif gait == 1:
            self.walk_progress[0] = 0
            self.walk_progress[1] = 1/2
            self.walk_progress[2] = 0
            self.walk_progress[3] = 1/2
            self.walk_progress[4] = 0
            self.walk_progress[5] = 1/2

            self.push_fraction = 3.1/6
            self.speed_multiplier = 1


        elif gait == 2:
            self.walk_progress[0] = 0
            self.walk_progress[1] = 1/6
            self.walk_progress[2] = 2/6
            self.walk_progress[3] = 5/6
            self.walk_progress[4] = 4/6
            self.walk_progress[5] = 3/6

            self.push_fraction = 5/6
            self.speed_multiplier = 0.3


    def gen_point(self, leg, walk_dir, walk_speed, turn_vector, gait, last_points, origin_point):
        self.gait_parameter(gait)
        #walk_dir = 0
        #walk_speed = 1
        #print(last_points)
        #walk_dir = 27
        walk_speed = operations.constrain(walk_speed, 0, 1)
        stepsize = (walk_speed - 0.20) * 1.2 + 0.04
        stepsize = stepsize *4
        #mount_angle = config.data["legMountAngle"][leg-1]
        #gait_parameter(gait)
        #turn_strength = operations.constrain((turn_strength-0.2)*1.25, 0, 1)
        if turn_vector[0] < 0:
            turn_strength = (turn_vector[0]+0.2)/0.8
            turn_strength = -(1 + turn_strength)
        else:
            turn_strength = (turn_vector[0]-0.2)/0.8
            turn_strength = 1 - turn_strength
        turn_strength = operations.constrain(turn_strength, -1, 1)
        #turn_strength = 0.4
        #print(turn_strength)
        turn_radius = (turn_strength*10)**5
        biggest_distance = 0
        for i in range(6):
            distance = math.sqrt((last_points[i][0] - (turn_radius * math.cos(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][i] + 180))))) ** 2 +
                                 (last_points[i][1] - (turn_radius * math.sin(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.cos(math.radians(config.data["legMountAngle"][i] + 180))))) ** 2)
            #print(f"new distance: {distance}")

            if distance > biggest_distance:
                biggest_distance = distance
        #print(biggest_distance)

        current_distance = math.sqrt((last_points[leg-1][0] - (turn_radius * math.cos(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][leg-1] + 180))))) ** 2 +
                                     (last_points[leg-1][1] - (turn_radius * math.sin(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.cos(math.radians(config.data["legMountAngle"][leg-1] + 180))))) ** 2)
        stepsize = stepsize * (current_distance/biggest_distance)*self.speed_multiplier
        #print(f"leg: {leg}, stepsize: {stepsize}")

        if (last_points[leg-1][0] - turn_radius * math.cos(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][leg-1] + 180)))) < 0:
            tangent_angle = math.degrees(math.atan(((last_points[leg-1][1] - (turn_radius * math.sin(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.cos(math.radians(config.data["legMountAngle"][leg-1] + 180)))))/
                                                    (last_points[leg-1][0] - (turn_radius * math.cos(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][leg-1] + 180))))))))
            #print(1)
        else:
            tangent_angle = math.degrees(math.atan(((last_points[leg-1][1] - (turn_radius * math.sin(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.cos(math.radians(config.data["legMountAngle"][leg-1] + 180)))))/
                                                    (last_points[leg-1][0] - (turn_radius * math.cos(math.radians(walk_dir)) + ((origin_point[0] + 120) * math.sin(math.radians(config.data["legMountAngle"][leg-1] + 180)))))))) + 180
            #print(2)
        #print(tangent_angle)
        #print(f"tangent angle: {tangent_angle}")
        #print()
        #print([stepsize*math.cos(math.radians(tangent_angle+90)), stepsize*math.sin(math.radians(tangent_angle+90))])
        new_point = [last_points[leg-1][0] + stepsize*math.cos(math.radians(tangent_angle+90)),last_points[leg-1][1] + stepsize*math.sin(math.radians(tangent_angle+90)), last_points[leg-1][2]]
        return [last_points[leg-1][0] + stepsize*math.cos(math.radians(tangent_angle+90)),last_points[leg-1][1] + stepsize*math.sin(math.radians(tangent_angle+90)), last_points[leg-1][2]]



