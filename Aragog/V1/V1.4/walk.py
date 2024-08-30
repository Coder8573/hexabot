import operations
import Bezier
import vectors
#from Aragog.V4.vectors import Vector3


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
        # self.distanceFromGround = -80
        self.strideMultiplier = [1, 1, 1, -1, -1, -1]
        self.rotationMultiplier = [-1, 0, 1, -1, 0 , 1]
        self.push_fraction = 3/6
        self.cycleProgress = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.legStates = [0, 0, 0, 0, 0, 0]
        self.current_gait = 1

        self.maxStrideLength = 200
        self.strideLengthMultiplier = 1.5
        self.globalRotationMultiplier = 0.55
        self.globalSpeedMultiplier = 0.55
        self.speed_multiplier = 0.8
        self.max_speed = 200
        self.liftHeight = 80
        self.lift_height_multiplier = 1.3
        self.max_step_length = 150

        self.origin_point = [180, 0, -80]
        self.cycleStartPoints = [[180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80]]
        self.current_point = [[180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80]]

    def gait_parameter(self, gait):
        if gait == 0:
            self.cycleProgress[0] = 0
            self.cycleProgress[1] = 0
            self.cycleProgress[2] = 0
            self.cycleProgress[3] = 0
            self.cycleProgress[4] = 0
            self.cycleProgress[5] = 0

            self.push_fraction = 3/6
            self.speed_multiplier = 0.8
            self.lift_height_multiplier = 1
            self.max_step_length = 240
            self.max_speed = 200


        elif gait == 1:
            self.cycleProgress[0] = 0
            self.cycleProgress[1] = 1/2
            self.cycleProgress[2] = 0
            self.cycleProgress[3] = 1/2
            self.cycleProgress[4] = 0
            self.cycleProgress[5] = 1/2

            self.push_fraction = 3.1/6
            self.speed_multiplier = 1
            self.lift_height_multiplier = 1.1
            self.max_step_length = 240
            self.max_speed = 200


        elif gait == 2:
            self.cycleProgress[0] = 0
            self.cycleProgress[1] = 1/6
            self.cycleProgress[2] = 2/6
            self.cycleProgress[3] = 5/6
            self.cycleProgress[4] = 4/6
            self.cycleProgress[5] = 3/6

            self.push_fraction = 5/6
            self.speed_multiplier = 1
            self.lift_height_multiplier = 1.3
            self.max_step_length = 150
            self.max_speed = 200




    #cycleStartPoints = [[180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80], [180, 0, -80]]
    def walk(self, joy1, joy2, gait):
        if self.current_gait != gait:
            print(f"gate changed to: {gait}")
            self.current_gait = gait
            self.gait_parameter(gait)

        forwardAmount = operations.constrain(operations.calc_hypotenuse(joy1[0], joy1[1]), 0, 100)
        turnAmount = joy2[0]

        progressChangeAmount = (max(abs(forwardAmount),abs(turnAmount)) * self.speed_multiplier) * self.globalSpeedMultiplier
        progressChangeAmount = operations.constrain(progressChangeAmount, 0, self.max_speed*self.globalSpeedMultiplier)/10000
        #print(progressChangeAmount)
        for i in range(6):
            self.cycleProgress[i] = (self.cycleProgress[i] + progressChangeAmount) % 1
        #print(self.cycleProgress)

        for leg in range(1, 7):
            self.current_point[leg-1] = self.gen_point(leg, self.cycleProgress[leg-1], joy1, joy2)

        #print(self.current_point)
        return self.current_point


    def setCycleStartPoints(self, leg):
        self.cycleStartPoints[leg-1] = self.current_point[leg-1]

    def gen_point(self, leg, t, joy1, joy2):
        joy1TargetMagnitude = operations.constrain(operations.calc_hypotenuse(joy1[0], joy1[1]), 0, 100)
        joy2TargetMagnitude = operations.constrain(operations.calc_hypotenuse(joy2[0], joy2[1]), 0, 100)

        joy1CurrentVector = joy1
        joy1CurrentMagnitude = joy1TargetMagnitude
        joy2CurrentVector = joy2
        joy2CurrentMagnitude = joy2TargetMagnitude

        forwardAmount = joy1CurrentMagnitude
        turnAmount = joy2CurrentVector[0]

        rotateStrideLength = joy2CurrentVector[0] * self.globalRotationMultiplier
        v = vectors.multi_with_point(joy1CurrentVector, [1, self.strideLengthMultiplier])
        v[1] = operations.constrain(v[1], -self.maxStrideLength/2, self.maxStrideLength/2)
        v = vectors.multi_with_val(v, self.globalSpeedMultiplier)

        weightSum = abs(forwardAmount) + abs(turnAmount)


        if t < self.push_fraction:
            if self.legStates[leg-1] != 1:
                self.legStates[leg - 1] = 1
                self.setCycleStartPoints(leg)
            # Propelling phase
            ControlPoint1 = self.cycleStartPoints[leg-1]
            ControlPoint2 = vectors.rotate([v[0] * self.strideMultiplier[leg - 1] + self.origin_point[0], -v[1] * self.strideMultiplier[leg - 1], self.origin_point[2]], self.rotationMultiplier[leg - 1] * 60, [self.origin_point[0], 0])
            straight_point = Bezier.get_point_on_curve_3([ControlPoint1, ControlPoint2], 2, operations.map_value(t, 0, self.push_fraction, 0, 1))

            RotateControlPoints1 = self.cycleStartPoints[leg-1]
            RotateControlPoints2 = [self.origin_point[0] + 40, 0, self.origin_point[2]]
            RotateControlPoints3 = [self.origin_point[0], rotateStrideLength, self.origin_point[2]]
            rotatePoint = Bezier.get_point_on_curve_3((RotateControlPoints1, RotateControlPoints2, RotateControlPoints3), 3, operations.map_value(t, 0, self.push_fraction, 0, 1))

            return vectors.divide_with_val(vectors.add_point(vectors.multi_with_val(straight_point, abs(forwardAmount)), vectors.multi_with_val(rotatePoint, abs(turnAmount))), weightSum)

        else:
            if self.legStates[leg-1] != 2:
                self.legStates[leg - 1] = 2
                #self.setCycleStartPoints(leg)
                self.setCycleStartPoints(leg)
                #self.cycleStartPoints[leg - 1] = self.current_point[leg - 1]
            #return [0, 0, 0]

            #ControlPoint1 = self.cycleStartPoints[leg-1]
            #ControlPoint2 = vectors.rotate([-v[0]*self.strideMultiplier[leg-1] + self.origin_point[0], v[1]*self.strideMultiplier[leg-1], self.origin_point[2]], self.rotationMultiplier[leg-1]*60, [self.origin_point[0], 0])
            #straight_point = Bezier.get_point_on_curve_3([ControlPoint1, ControlPoint2], 2, operations.map_value(t, self.push_fraction, 1, 0, 1))
            #RotateControlPoints1 = self.cycleStartPoints[leg-1]
            #RotateControlPoints2 = [self.origin_point[0] + 40, 0, self.origin_point[2]]
            #RotateControlPoints3 = [self.origin_point[0], rotateStrideLength, self.origin_point[2]]
            #rotatePoint = Bezier.get_point_on_curve_3((RotateControlPoints1, RotateControlPoints2, RotateControlPoints3), 3, operations.map_value(t, self.push_fraction, 1, 0, 1))
            #return vectors.divide_with_val(vectors.add_point(vectors.multi_with_val(straight_point, abs(forwardAmount)), vectors.multi_with_val(rotatePoint, abs(turnAmount))), weightSum)

            ControlPoint1 = self.cycleStartPoints[leg-1]
            #ControlPoint2 = vectors.add_point(self.cycleStartPoints[leg - 1], [0, 0, self.liftHeight*self.lift_height_multiplier])
            ControlPoint2 = vectors.add_point(self.cycleStartPoints[leg - 1], [0, 0, self.liftHeight * self.lift_height_multiplier])
            #ControlPoint2 = [0, 0, self.origin_point[2]+self.liftHeight*self.lift_height_multiplier]
            #ControlPoints[2] = Vector3(-v.x * strideMultiplier[leg] + distanceFromCenter, (v.y + strideOvershoot) * strideMultiplier[leg], distanceFromGround + landHeight).rotate(legPlacementAngle * rotationMultiplier[leg], Vector2(distanceFromCenter,0));
            #ControlPoint3 = vectors.rotate([v[0]*self.strideMultiplier[leg-1] + self.origin_point[0], -v[1]*self.strideMultiplier[leg-1], self.origin_point[2]], self.rotationMultiplier[leg-1]*60, [self.origin_point[0], 0])
            #ControlPoints[3] = Vector3(-v.x * strideMultiplier[leg] + distanceFromCenter, v.y * strideMultiplier[leg], distanceFromGround).rotate(legPlacementAngle * rotationMultiplier[leg], Vector2(distanceFromCenter,0));
            ControlPoint3 = vectors.rotate([-v[0] * self.strideMultiplier[leg - 1] + self.origin_point[0], v[1] * self.strideMultiplier[leg - 1], self.origin_point[2]], self.rotationMultiplier[leg - 1] * 60, [self.origin_point[0], 0])
            print([ControlPoint1, ControlPoint2, ControlPoint3])
            straight_point = Bezier.get_point_on_curve_3([ControlPoint1, ControlPoint2, ControlPoint3], 3, operations.map_value(t, self.push_fraction, 1, 0, 1))

            RotateControlPoints1 = self.cycleStartPoints[leg-1]
            #RotateControlPoints2 = [self.origin_point[0] + 40, 0, self.origin_point[2]+(self.liftHeight*self.lift_height_multiplier)]
            RotateControlPoints2 = vectors.add_point(self.cycleStartPoints[leg - 1], [0, 0, self.liftHeight * self.lift_height_multiplier])
            RotateControlPoints3 = [self.origin_point[0], -rotateStrideLength, self.origin_point[2]]
            rotatePoint = Bezier.get_point_on_curve_3((RotateControlPoints1, RotateControlPoints2, RotateControlPoints3), 3, operations.map_value(t, self.push_fraction, 1, 0, 1))

            return vectors.divide_with_val(vectors.add_point(vectors.multi_with_val(straight_point, abs(forwardAmount)), vectors.multi_with_val(rotatePoint, abs(turnAmount))), weightSum)


        #gerade:
            # anfangspunkt
            #