import math

import operations
import Bezier
import vectors
import config


class Walk_Class:
    def __init__(self):
        # self.forwardAmount
        # self.turnAmount
        # self.liftHeightMultiplier
        # self.liftHeight
        # self.strideOvershoot
        # self.landHeight
        # self.weightSum
        # self.distanceFromCenter = 180
        # self.distanceFromGround = -
        self.push_fraction = 3/6
        self.walk_progress = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.legStates = [0, 0, 0, 0, 0, 0]
        self.current_gait = 0

        self.step_length = config.data["step_length"]
        self.step_height = config.data["step_height"]
        self.step_size_multiplier = 1
        self.speed_multiplier = 1.6
        self.step_height_multiplier = 1

        self.origin_point = config.data["origin_point"]
        self.current_point = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def gait_parameter(self, gait):
        if gait == 0:
            # Mono Gait
            self.walk_progress[0] = 0
            self.walk_progress[1] = 0
            self.walk_progress[2] = 0
            self.walk_progress[3] = 0
            self.walk_progress[4] = 0
            self.walk_progress[5] = 0

            self.push_fraction = 3/6
            self.step_size_multiplier = 1
            self.speed_multiplier = 1
            self.step_height_multiplier = 1


        elif gait == 1:
            # Tri Gait
            self.walk_progress[0] = 0
            self.walk_progress[1] = 1 / 2
            self.walk_progress[2] = 0
            self.walk_progress[3] = 1 / 2
            self.walk_progress[4] = 0
            self.walk_progress[5] = 1 / 2

            self.push_fraction = 3.1/6
            self.step_size_multiplier = 1
            self.speed_multiplier = 1.2
            self.step_height_multiplier = 1


        elif gait == 2:
            # Wave Gait
            self.walk_progress[0] = 0
            self.walk_progress[1] = 1 / 6
            self.walk_progress[2] = 2 / 6
            self.walk_progress[3] = 3 / 6
            self.walk_progress[4] = 4 / 6
            self.walk_progress[5] = 5 / 6

            self.push_fraction = 5/6
            self.step_size_multiplier = 1
            self.speed_multiplier = 0.4
            self.step_height_multiplier = 1

        elif gait == 3:
            # Ripple Gait
            self.walk_progress[0] = 0
            self.walk_progress[1] = 4 / 6
            self.walk_progress[2] = 2 / 6
            self.walk_progress[3] = 5 / 6
            self.walk_progress[4] = 1 / 6
            self.walk_progress[5] = 3 / 6

            self.push_fraction = 3.2/6
            self.step_size_multiplier = 1
            self.speed_multiplier = 1.4
            self.step_height_multiplier = 0.6

        elif gait == 4:
            # Bi Gait
            self.walk_progress[0] = 0
            self.walk_progress[1] = 1 / 3
            self.walk_progress[2] = 2 / 3
            self.walk_progress[3] = 0
            self.walk_progress[4] = 1 / 3
            self.walk_progress[5] = 2 / 3

            self.push_fraction = 2.1/6
            self.step_size_multiplier = 1
            self.speed_multiplier = 1
            self.step_height_multiplier = 1

        elif gait == 5:
            # Quad Gait
            self.walk_progress[0] = 0
            self.walk_progress[1] = 1 / 3
            self.walk_progress[2] = 2 / 3
            self.walk_progress[3] = 0
            self.walk_progress[4] = 1 / 3
            self.walk_progress[5] = 2 / 3

            self.push_fraction = 4.1/6
            self.step_size_multiplier = 1
            self.speed_multiplier = 1
            self.step_height_multiplier = 1




    #cycleStartPoints = [[180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80]]
    def walk(self, joy1, joy2, gait):
        if self.current_gait != gait:
            print(f"gate changed to: {gait}")
            self.current_gait = gait
            self.gait_parameter(gait)

        forward_amount = operations.constrain(operations.calc_hypotenuse(joy1[0], joy1[1]), 0, 1)
        turn_amount = joy2[0]

        progressChangeAmount = (max(abs(forward_amount),abs(turn_amount)) * self.speed_multiplier)/200
        #print(progressChangeAmount)
        for i in range(6):
            self.walk_progress[i] = (self.walk_progress[i] + progressChangeAmount) % 1
        #print(self.cycleProgress)

        for leg in range(1, 7):
            self.current_point[leg-1] = self.gen_point(leg, self.walk_progress[leg - 1], joy1, joy2)

        #print(self.current_point)
        return self.current_point

    def get_rotations_angle(self, leg, x):
        if x >= 0:
            rotation_point = [(1-x)*(self.origin_point[0]+120)*2, 0]
        else:
            rotation_point = [(1+x)*(self.origin_point[0]+120)*(-2), 0]

        max_distance = 0
        for i in range(6):
            distance = vectors.distance(
                vectors.rotate([self.origin_point[0] + 120, self.origin_point[1]], config.data["legMountAngle"][i] - 90, [0, 0]), rotation_point)
            if distance > max_distance:
                max_distance = distance
        current_distance = vectors.distance(vectors.rotate([self.origin_point[0] + 120, self.origin_point[1]], config.data["legMountAngle"][leg - 1] - 90, [0, 0]), rotation_point)
        if x < 0:
            rotation_step_length = -(self.step_length * (current_distance / max_distance))
        else:
            rotation_step_length = self.step_length * (current_distance / max_distance)



        if (math.sin(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120))-rotation_point[0] > 0:
            rotation_angle = 270 - math.degrees(math.atan((math.cos(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120)-rotation_point[1])/(math.sin(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120)-rotation_point[0])))
        elif (math.sin(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120))-rotation_point[0] < 0:
            rotation_angle = 90 - math.degrees(math.atan((math.cos(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120)-rotation_point[1])/(math.sin(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120)-rotation_point[0])))
        else:
            rotation_angle = 0
        rotation_angle = -rotation_angle+config.data["legMountAngle"][leg-1]
        #print(leg, current_distance, max_distance, x)
        #rotation_angle = 0

        ##print(rotation_point)
        #max_distance = 0
        #for i in range(6):
        #    distance = vectors.distance(vectors.rotate([self.origin_point[0]+120, self.origin_point[1]], config.data["legMountAngle"][i]+90, [0, 0]), rotation_point)
        #    if distance > max_distance:
        #        max_distance = distance
        #current_distance = vectors.distance(vectors.rotate([self.origin_point[0]+120, self.origin_point[1]], config.data["legMountAngle"][leg-1]+90, [0, 0]), rotation_point)
#
        #rotation_step_length = self.step_length*(current_distance/max_distance)
        #if 0 <= ((math.sin(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120))-rotation_point[0]):
        #    rotation_angle = 270-math.degrees(math.atan((rotation_point[1]-(math.cos(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120)))/(rotation_point[0]-(math.sin(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120)))))
        ##elif 0 > ((math.sin(math.radians(config.data["legMountAngle"][leg-1])*(self.origin_point[0]+120)))-rotation_point[0]):
        #else:
        #    rotation_angle = 90-math.degrees(math.atan((rotation_point[1]-(math.cos(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120)))/(rotation_point[0]-(math.sin(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120)))))
        #rotation_angle = rotation_angle - config.data["legMountAngle"][leg-1]
        #else:
        #    print((math.sin(math.radians(config.data["legMountAngle"][leg-1]))*(self.origin_point[0]+120))-rotation_point[0])
        #    print()
        #    rotation_angle = 360
        return rotation_angle, rotation_step_length

    def gen_point(self, leg, t, joy1, joy2):
        joy1_magnitude = operations.constrain(operations.calc_hypotenuse(joy1[0], joy1[1]), 0, 100)
        joy2_magnitude = operations.constrain(operations.calc_hypotenuse(joy2[0], joy2[1]), 0, 100)

        if joy1[0] > 0:
            walk_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 90
        elif joy1[0] < 0:
            walk_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 270
        else:
            if joy1[1] >= 0:
                walk_dir = 180
            else:
                walk_dir = 0
        #print(walk_dir)
        forward_amount = joy1_magnitude
        turn_amount = joy2[0]

        weightSum = abs(forward_amount) + abs(turn_amount)


        if t < self.push_fraction:
            if self.legStates[leg-1] != 1:
                self.legStates[leg - 1] = 1

            straight_point_1 = vectors.add_point(
                vectors.rotate([0, 0.5 * self.step_length, 0], -walk_dir + config.data["legMountAngle"][leg - 1] - 90, [0, 0]), self.origin_point)
            straight_point_2 = vectors.add_point(
                vectors.rotate([0, -0.5 * self.step_length, 0], -walk_dir + config.data["legMountAngle"][leg - 1] - 90, [0, 0]), self.origin_point)
            straight_point = Bezier.get_point_on_curve_3([straight_point_1, straight_point_2], 2, operations.map_value(t, 0, self.push_fraction, 0, 1))
            #straight_point = [0, 0, 0]

            rotation_angle, rotation_step_length = self.get_rotations_angle(leg, joy2[0])
            #print(leg, rotation_angle, rotation_step_length)
            rotate_point_1 = vectors.add_point(
                vectors.rotate([0, 0.5 * rotation_step_length, 0], rotation_angle, [0, 0]), self.origin_point)
            rotate_point_2 = vectors.add_point(
                vectors.rotate([0, -0.5 * rotation_step_length, 0], rotation_angle, [0, 0]), self.origin_point)
            rotate_point = Bezier.get_point_on_curve_3((rotate_point_1, rotate_point_2), 2, operations.map_value(t, 0, self.push_fraction, 0, 1))

            return vectors.divide_with_val(
                vectors.add_point(vectors.multi_with_val(straight_point, abs(forward_amount)), vectors.multi_with_val(rotate_point, abs(turn_amount))), weightSum)

        else:
            if self.legStates[leg-1] != 2:
                self.legStates[leg - 1] = 2

            #print(walk_dir)
            straight_point_1 = vectors.add_point(
                vectors.rotate([0, -0.5 * self.step_length, 0], -walk_dir + config.data["legMountAngle"][leg - 1] - 90, [0, 0]), self.origin_point)
            straight_point_2 = vectors.add_point(self.origin_point, [0, 0, self.step_height * self.step_height_multiplier])
            straight_point_3 = vectors.add_point(
                vectors.rotate([0, 0.5 * self.step_length, 0], -walk_dir + config.data["legMountAngle"][leg - 1] - 90, [0, 0]), self.origin_point)
            straight_point = Bezier.get_point_on_curve_3([straight_point_1, straight_point_2, straight_point_3], 3, operations.map_value(t, self.push_fraction, 1, 0, 1))
            #straight_point = [0, 0, 0]

            rotation_angle, rotation_step_length = self.get_rotations_angle(leg, joy2[0])
            rotate_point_1 = vectors.add_point(
                vectors.rotate([0, -0.5 * rotation_step_length, 0], rotation_angle, [0, 0]), self.origin_point)
            rotate_point_2 = vectors.add_point(self.origin_point, [0, 0, self.step_height * self.step_height_multiplier])
            rotate_point_3 = vectors.add_point(
                vectors.rotate([0, 0.5 * rotation_step_length, 0], rotation_angle, [0, 0]), self.origin_point)
            rotate_point = Bezier.get_point_on_curve_3((rotate_point_1, rotate_point_2, rotate_point_3), 3, operations.map_value(t, self.push_fraction, 1, 0, 1))
            return vectors.divide_with_val(
                vectors.add_point(vectors.multi_with_val(straight_point, abs(forward_amount)), vectors.multi_with_val(rotate_point, abs(turn_amount))), weightSum)

#
            #straight_point_1 = [0, 0, 0]
            #straight_point_2 = [0, 0, 0]
            #straight_point = Bezier.get_point_on_curve_3([straight_point_1, straight_point_2], 2, operations.map_value(t, 0, self.push_fraction, 0, 1))
            #rotate_point_1 = [0, 0, 0]
            #rotate_point_2 = [0, 0, 0]
            #rotate_point_3 = [0, 0, 0]
            #rotatePoint = Bezier.get_point_on_curve_3((rotate_point_1, rotate_point_2, rotate_point_3), 3, operations.map_value(t, 0, self.push_fraction, 0, 1))
            #return vectors.divide_with_val(vectors.add_point(vectors.multi_with_val(straight_point, abs(forwardAmount)), vectors.multi_with_val(rotatePoint, abs(turnAmount))), weightSum)





