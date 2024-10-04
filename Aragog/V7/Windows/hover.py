import math

import operations
import vectors
import config


class Hover_Class:
    def __init__(self):
        self.step_length = config.data["hover_step_length"]
        self.step_height = config.data["hover_step_height"]
        self.step_size_multiplier = 1
        self.speed_multiplier = 1

        self.origin_point = config.data["origin_point"]
        self.leg_points = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.points = [self.origin_point, self.origin_point, self.origin_point, self.origin_point, self.origin_point, self.origin_point]

    def hover(self, joy1, joy2):

        for leg in range(1, 7):
            self.points[leg-1] = self.gen_point(leg, joy1, joy2)

            #print(self.points)
        return self.points

    def gen_point(self, leg, joy1, joy2):
        joy1_magnitude = operations.constrain(operations.map_value(operations.calc_hypotenuse(joy1[0], joy1[1]), 0.2, 1, 0, 1), 0, 1)
        joy2_magnitude = operations.constrain(operations.map_value(operations.calc_hypotenuse(joy2[0], joy2[1]), 0.2, 1, 0, 1), 0, 1)

        if joy1[0] > 0:
            move_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 90
        elif joy1[0] < 0:
            move_dir = math.degrees(math.atan(joy1[1] / joy1[0])) + 270
        else:
            if joy1[1] >= 0:
                move_dir = 180
            else:
                move_dir = 0

        new_point = vectors.add_point(self.points[leg-1], [joy1_magnitude * math.cos(math.radians(-move_dir+config.data["legMountAngle"][leg-1]+180)), joy1_magnitude * math.sin(math.radians(-move_dir+config.data["legMountAngle"][leg-1]+180)), 0])
        #new_point = vectors.add_point(self.points[leg-1], [joy1[0]*math.cos(math.radians(config.data["legMountAngle"][leg-1])), joy1[1]*math.sin(math.radians(config.data["legMountAngle"][leg-1])), 0])
        rotation_point_y = vectors.rotate(vectors.multi_with_val([new_point[0], new_point[2]], abs(math.cos(math.radians(config.data["legMountAngle"][leg-1]+90)))), joy2[0]*0.02, [-120, 0])
        new_point = [rotation_point_y[0], new_point[1], rotation_point_y[1]]
        #print(new_point)
        #if self.is_point_valid(new_point, self.origin_point, self.step_length):
        #    return new_point
        #else:
        #    return self.points[leg-1]

        return new_point

    def is_point_valid(self, point, origin_point, step_length):
        if vectors.distance(point, origin_point) > step_length:
            return False
        else:
            return True