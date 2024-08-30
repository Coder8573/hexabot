import math

import config


class Calc:
    def __init__(self):
        self.legJoint1ToJoint2 = config.data["legJoint1ToJoint2"]
        self.legJoint2ToJoint3 = config.data["legJoint2ToJoint3"]
        self.legJoint3ToTip = config.data["legJoint3ToTip"]

    def calc_ang_m1(self, coord):
        x = coord[0]
        y = coord[1]
        if(x == 0 and y == 0):
            return 180
        else:
            return math.degrees(math.acos(y/(math.sqrt(x**2+y**2))))+90

    # calculate inital Angle (x/z)
    def calc_initial_angle(self, coord, w1):
        x = coord[0]
        y = coord[1]
        z = coord[2]

        if z != 0:
            if z > 0:
                return math.degrees(math.atan(math.sqrt((x-math.sin(w1)*self.legJoint1ToJoint2)**2+(y-math.cos(w1)*self.legJoint1ToJoint2)**2)/z))-180
            else:
                return math.degrees(math.atan(math.sqrt((x-math.sin(w1)*self.legJoint1ToJoint2)**2+(y-math.cos(w1)*self.legJoint1ToJoint2)**2)/z))
        else:
            return 0

    def calc_ang_m2(self, coord, M1):
        x = coord[0]
        y = coord[1]
        z = coord[2]
        w1 = math.radians(M1-90)

        if (x >= self.legJoint1ToJoint2):
            WM2 = math.degrees(math.acos(
                (((x - math.sin(w1) * self.legJoint1ToJoint2) ** 2 + (y - math.cos(w1) * self.legJoint1ToJoint2) ** 2 + z ** 2) + self.legJoint2ToJoint3 ** 2 - self.legJoint3ToTip ** 2) / ( 2 * self.legJoint2ToJoint3 * math.sqrt(
                        (x - math.sin(w1) * self.legJoint1ToJoint2) ** 2 + (y - math.cos(w1) * self.legJoint1ToJoint2) ** 2 + z ** 2)))) - self.calc_initial_angle(coord, w1)
        else:
            WM2 = math.degrees(math.acos(
                (((x - math.sin(w1) * self.legJoint1ToJoint2) ** 2 + (y - math.cos(w1) * self.legJoint1ToJoint2) ** 2 + z ** 2) + self.legJoint2ToJoint3 ** 2 - self.legJoint3ToTip ** 2) / (
                            2 * self.legJoint2ToJoint3 * math.sqrt( (x - math.sin(w1) * self.legJoint1ToJoint2) ** 2 + (y - math.cos(w1) * self.legJoint1ToJoint2) ** 2 + z ** 2)))) + self.calc_initial_angle(coord, w1)
        return WM2+90

    def calc_ang_m3(self, coord, M1):
        x = coord[0]
        y = coord[1]
        z = coord[2]
        w1 = math.radians(M1-90)
        return 90-math.degrees(math.asin((self.legJoint2ToJoint3**2+self.legJoint3ToTip**2-((x-math.sin(w1)*self.legJoint1ToJoint2)**2+(y-math.cos(w1)*self.legJoint1ToJoint2)**2+z**2))/(2*self.legJoint2ToJoint3*self.legJoint3ToTip)))

    def abs_coord_to_local_coord(self, coord, leg):
        # Koordinaten zum ursprung verschieben
        coord = [coord[0] - config.data["legMountX"][leg-1], coord[1] - config.data["legMountY"][leg-1], coord[2]]
        # Koordinaten um Ursprung drehen
        if coord[0] < 0:
            coord = [math.cos(math.radians(-config.data["legMountAngle"][leg-1])+math.atan(coord[1]/coord[0])+math.pi)*math.sqrt(coord[0]**2+coord[1]**2),
                     math.sin(math.radians(-config.data["legMountAngle"][leg-1])+math.atan(coord[1]/coord[0])+math.pi)*math.sqrt(coord[0]**2+coord[1]**2),
                     coord[2]]
        elif coord[0] > 0:
            coord = [math.cos(math.radians(-config.data["legMountAngle"][leg-1])+math.atan(coord[1]/coord[0]))*math.sqrt(coord[0]**2+coord[1]**2),
                     math.sin(math.radians(-config.data["legMountAngle"][leg-1])+math.atan(coord[1]/coord[0]))*math.sqrt(coord[0]**2+coord[1]**2),
                     coord[2]]
        elif coord[0] == 0:
            coord = [math.cos(math.radians(-config.data["legMountAngle"][leg-1])+0.5*math.pi)*coord[1],
                     math.sin(math.radians(-config.data["legMountAngle"][leg-1])+0.5*math.pi)*coord[1],
                     coord[2]]
        #print(coord)
        return coord

    def local_coord_to_abs_coord(self, coord, leg):
        #point = [math.sin(math.radians(dir))*point[0], math.cos(math.radians(dir))*point[0], point[1]]
        if coord[0] > 0:
            displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1])+math.atan(coord[1]/coord[0]))*math.sqrt(coord[0]**2+coord[1]**2) + config.data["legMountX"][leg-1],
                                  math.sin(math.radians(config.data["legMountAngle"][leg-1])+math.atan(coord[1]/coord[0]))*math.sqrt(coord[0]**2+coord[1]**2) + config.data["legMountY"][leg-1],
                                  coord[2]]
        elif coord[0] < 0:
            displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1])+math.atan(coord[1]/coord[0])+0.5*math.pi)*math.sqrt(coord[0]**2+coord[1]**2) + config.data["legMountX"][leg-1],
                                  math.sin(math.radians(config.data["legMountAngle"][leg-1])+math.atan(coord[1]/coord[0])+0.5*math.pi)*math.sqrt(coord[0]**2+coord[1]**2) + config.data["legMountY"][leg-1],
                                  coord[2]]
        else:
            displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1]))*coord[1] + config.data["legMountX"][leg-1],
                                  math.sin(math.radians(config.data["legMountAngle"][leg-1]))*coord[1] + config.data["legMountY"][leg-1],
                                  coord[2]]
        point = [coord[0] + displacement_point[0], coord[1] + displacement_point[1], coord[2] + displacement_point[2]]
        return point


    def local_coord_to_steps(self, coord, leg):
        M1 = self.calc_ang_m1(coord)
        M2 = self.calc_ang_m2(coord, M1)
        M3 = self.calc_ang_m3(coord, M1)
        #print([M1, M2, M3])
        return [int(round(((-180*(config.data["legScale"][leg-1][0]-1))+M1*config.data["legScale"][leg-1][0])*(512/45), 0)),
                int(round(((-180*(config.data["legScale"][leg-1][1]-1))+M2*config.data["legScale"][leg-1][1])*(512/45), 0)),
                int(round(((-180*(config.data["legScale"][leg-1][2]-1))+M3*config.data["legScale"][leg-1][2])*(512/45), 0))]

    def abs_coord_to_steps(self, coord, leg):
        local_coord = self.abs_coord_to_local_coord(coord, leg)
        return self.local_coord_to_steps(local_coord, leg)


    def angels_to_coord(self, M1, M2, M3, leg):
        M1 = 360-((-180*(config.data["legScale"][leg-1][0]-1))+M1*config.data["legScale"][leg-1][0])
        M2 = 360-((-180*(config.data["legScale"][leg-1][1]-1))+M2*config.data["legScale"][leg-1][1])
        M3 = 360-((-180*(config.data["legScale"][leg-1][2]-1))+M3*config.data["legScale"][leg-1][2])
        #print([M1, M2, M3])
        x = math.cos(math.radians(M1-180))*(self.legJoint1ToJoint2+self.legJoint2ToJoint3*math.cos(math.radians(M2-180))+self.legJoint3ToTip*math.cos(math.radians(M2+M3)))
        y = math.sin(math.radians(M1))*(self.legJoint1ToJoint2+self.legJoint2ToJoint3*math.cos(math.radians(M2-180))+self.legJoint3ToTip*math.cos(math.radians(M2+M3)))
        z = self.legJoint2ToJoint3*math.sin(math.radians(M2-180))+self.legJoint3ToTip*math.sin(math.radians(M2+M3))
        return [round(x, 4), round(y, 4),round(z, 4)]

