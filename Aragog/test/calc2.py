

import math

p = 120
q = 160
o = 40



# calculate Angle for Motor 1
def CWM1(coord):
    x = coord[0]
    y = coord[1]
    if(x != 0 and y != 0):
        return math.degrees(math.acos(y/(math.sqrt(x**2+y**2))))+90
    else:
        return 180

# calculate Angle for Motor 2
def CWM2(coord):
    x = coord[0]
    y = coord[1]
    z = coord[2]
    if (x != 0 and y != 0):
        w1 = math.acos(y/(math.sqrt(x**2+y**2)))
    else:
        w1 = 0

    if x >= o and z > 0:
        return (math.degrees(math.acos((((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2)+p**2-q**2)/(2*p*math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2))))
                - math.degrees(math.atan(math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2)/z))+270)
    elif x >= o and z < 0:
        return (math.degrees(math.acos((((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2)+p**2-q**2)/(2*p*math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2))))
                - math.degrees(math.atan(math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2)/z)))
    elif x >= o and z == 0:
        return (math.degrees(math.acos((((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2)+p**2-q**2)/(2*p*math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2))))
                + 90)
    elif x < o and z > 0:
        return (math.degrees(math.acos((((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2)+p**2-q**2)/(2*p*math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2))))
                + math.degrees(math.atan(math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2)/z))+270)
    elif x < o and z < 0:
        return (math.degrees(math.acos((((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2)+p**2-q**2)/(2*p*math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2))))
                + math.degrees(math.atan(math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2)/z)))
    elif x < o and z < 0:
        return (math.degrees(math.acos((((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2)+p**2-q**2)/(2*p*math.sqrt((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2))))
                + 90)
    elif x == 0 and y == 0 and z == 0:
        return 180

# calculate Angle for Motor 3
def CWM3(coord):
    x = coord[0]
    y = coord[1]
    z = coord[2]
    if (x != 0 and y != 0):
        w1 = math.acos(y / (math.sqrt(x ** 2 + y ** 2)))
    else:
        w1 = 0
    return 90-math.degrees(math.asin((p**2+q**2-((x-math.sin(w1)*o)**2+(y-math.cos(w1)*o)**2+z**2))/(2*p*q)))

def calc(coord, leg):
    W1 = CWM1(coord)
    print(W1)
    W2 = CWM2(coord)
    print(W2)
    W3 = CWM3(coord)
    print(W3)

    if (leg % 2 == 1):
        return [int(round(W1, 0)), int(round(360-W2, 0)), int(round(360-W3, 0))]
    else:
        return [int(round(W1, 0)), int(round(W2, 0)), int(round(W3, 0))]

def angles_to_steps(angles):
     return [int(round(angles[0]*(512/45), 0)), int(round(angles[1]*(512/45), 0)), int(round(angles[2]*(512/45), 0))]




#calc([240, 0 ,60], 1)