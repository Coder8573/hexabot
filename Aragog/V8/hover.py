import math

import operations
import vectors
import config
import kinematics


class Hover_Class:
    def __init__(self):
        self.step_length = config.data["hover_step_length"]
        self.step_height = config.data["hover_step_height"]
        self.step_size_multiplier = 1
        self.speed_multiplier = 1

        self.origin_point = config.data["origin_point"]
        self.leg_points = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.points = [self.origin_point, self.origin_point, self.origin_point, self.origin_point, self.origin_point, self.origin_point]

    def hover(self, joy1, joy2, l2, r2, gait):
        if gait == -1:
            for leg in range(1, 7):
                self.points[leg - 1] = self.gen_relative_point(leg, joy1, joy2, l2, r2)

        elif gait == -2:
            for leg in range(1, 7):
                self.points[leg - 1] = self.gen_live_point(leg, joy1, joy2, l2, r2)


        return self.points


    def gen_relative_point(self, leg, joy1, joy2, l2, r2):
        joy1_magnitude = operations.constrain(
            operations.map_value(operations.calc_hypotenuse(joy1[0], joy1[1]), 0.2, 1, 0, 1), 0, 1)
        joy2_magnitude = operations.constrain(
            operations.map_value(operations.calc_hypotenuse(joy2[0], joy2[1]), 0.2, 1, 0, 1), 0, 1)

        if joy1[0] > 0:
            move_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 90
        elif joy1[0] < 0:
            move_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 270
        else:
            if joy1[1] >= 0:
                move_dir = 180
            else:
                move_dir = 0


        displacement = [self.speed_multiplier*joy1_magnitude * math.cos(math.radians(-move_dir + config.data["legMountAngle"][leg - 1] + 180)),
                        self.speed_multiplier*joy1_magnitude * math.sin(math.radians(-move_dir + config.data["legMountAngle"][leg - 1] + 180)),
                        self.speed_multiplier*((1+l2)-(1+r2))*0.5]
        rotation = 0

        new_point = vectors.add_point(self.points[leg-1], displacement)
        # new_point = vectors.add_point(self.points[leg - 1], [joy1_magnitude * math.cos(math.radians(-move_dir + config.data["legMountAngle"][leg - 1] + 180)), joy1_magnitude * math.sin(math.radians(-move_dir +
        #                                                                                                                                                                                               config.data["legMountAngle"][leg - 1] + 180)), 0])
        # #new_point = vectors.add_point(self.points[leg-1], [joy1[0]*math.cos(math.radians(config.data["legMountAngle"][leg-1])), joy1[1]*math.sin(math.radians(config.data["legMountAngle"][leg-1])), 0])
        # rotation_point_y = vectors.rotate(vectors.multi_with_val([new_point[0], new_point[2]], abs(math.cos(math.radians(
        #     config.data["legMountAngle"][leg - 1] + 90)))), joy2[0] * 0.02, [-120, 0])
        # new_point = [rotation_point_y[0], new_point[1], rotation_point_y[1]]
        # #print(new_point)
        if self.is_point_valid(new_point, self.origin_point, self.step_length):
            return new_point
        else:
            return self.points[leg-1]


    def gen_live_point(self, leg, joy1, joy2, l2, r2):
        joy1_magnitude = operations.constrain(
            operations.map_value(operations.calc_hypotenuse(joy1[0], joy1[1]), 0.2, 1, 0, 1), 0, 1)
        joy2_magnitude = operations.constrain(
            operations.map_value(operations.calc_hypotenuse(joy2[0], joy2[1]), 0.2, 1, 0, 1), 0, 1)

        if joy1[0] > 0:
            move_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 90
        elif joy1[0] < 0:
            move_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 270
        else:
            if joy1[1] >= 0:
                move_dir = 180
            else:
                move_dir = 0


        displacement = [config.data["hover_step_length"] * joy1_magnitude * math.cos(math.radians(-move_dir + config.data["legMountAngle"][leg - 1] + 180)),
                         config.data["hover_step_length"] * joy1_magnitude * math.sin(math.radians(-move_dir + config.data["legMountAngle"][leg - 1] + 180)),
                         (1+l2)*config.data["hover_step_height"]-(1+r2)*config.data["hover_step_height"]]

        temp_point = [config.data["legMountX"][leg-1] + vectors.rotate(self.origin_point[0:1], -config.data["legMountAngle"][leg - 1]-90, [0, 0]),
                      config.data["legMountY"][leg-1] + vectors.rotate(self.origin_point[0:1], -config.data["legMountAngle"][leg - 1]-90, [0, 0]),
                      0]

        rotation = [temp_point[0], vectors.rotate(temp_point[1:2], joy2[0]*20, [0, 0])]

        new_point = vectors.add_point(rotation, displacement)
        # new_point = vectors.add_point(self.points[leg - 1], [joy1_magnitude * math.cos(math.radians(-move_dir + config.data["legMountAngle"][leg - 1] + 180)), joy1_magnitude * math.sin(math.radians(-move_dir +
        #                                                                                                                                                                                               config.data["legMountAngle"][leg - 1] + 180)), 0])
        # #new_point = vectors.add_point(self.points[leg-1], [joy1[0]*math.cos(math.radians(config.data["legMountAngle"][leg-1])), joy1[1]*math.sin(math.radians(config.data["legMountAngle"][leg-1])), 0])
        # rotation_point_y = vectors.rotate(vectors.multi_with_val([new_point[0], new_point[2]], abs(math.cos(math.radians(
        #     config.data["legMountAngle"][leg - 1] + 90)))), joy2[0] * 0.02, [-120, 0])
        # new_point = [rotation_point_y[0], new_point[1], rotation_point_y[1]]
        # #print(new_point)
        if self.is_point_valid(new_point, self.origin_point, self.step_length):
            return new_point
        else:
            return self.points[leg-1]


    def is_point_valid(self, point, origin_point, step_length):
        if vectors.distance(point, origin_point) > step_length:
            return False
        else:
            return True