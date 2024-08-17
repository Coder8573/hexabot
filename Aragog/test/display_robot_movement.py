import matplotlib.pyplot as plt
import time
import serial
import math


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return (~checksum) & 0xFF

def read_pos():
    packet = [255, 255, 254, 0, 0x82, 0x38, 0x02]
    for i in range(0, 18):
        packet.append(i + 1)
    packet[3] = len(packet[3:])
    packet.append(calculate_checksum(packet) - 2)
    ser.write(bytearray(packet))
    packet = []
    while not ser.in_waiting:
        pass
    while ser.in_waiting:
        packet.append(int.from_bytes(ser.read(), "little"))
        time.sleep(0.0000000001)
    seperate_motor_packets = []
    return_package = []
    for i in range(int(len(packet) / (packet[3] + 4))):
        seperate_motor_packets.append(packet[(packet[3] + 4) * i:(packet[3] + 4) * (i + 1)])
    for motor_packet in seperate_motor_packets:
        #print(f"""{motor_packet}; pos: {motor_packet[5] + motor_packet[6] * 256}steps; {(motor_packet[5] + motor_packet[6] * 256) * (45 / 512)}deg """)
        return_package.append((motor_packet[5] + motor_packet[6] * 256) * (45 / 512))
    return return_package

def angels_to_coord(M1, M2, M3, leg):
    M1 = 360-((-180*(data["legScale"][leg-1][0]-1))+M1*data["legScale"][leg-1][0])
    M2 = 360-((-180*(data["legScale"][leg-1][1]-1))+M2*data["legScale"][leg-1][1])
    M3 = 360-((-180*(data["legScale"][leg-1][2]-1))+M3*data["legScale"][leg-1][2])
    #print([M1, M2, M3])
    x = math.cos(math.radians(M1-180))*(data["legJoint1ToJoint2"]+data["legJoint2ToJoint3"]*math.cos(math.radians(M2-180))+data["legJoint3ToTip"]*math.cos(math.radians(M2+M3)))
    y = math.sin(math.radians(M1))*(data["legJoint1ToJoint2"]+data["legJoint2ToJoint3"]*math.cos(math.radians(M2-180))+data["legJoint3ToTip"]*math.cos(math.radians(M2+M3)))
    z = data["legJoint2ToJoint3"]*math.sin(math.radians(M2-180))+data["legJoint3ToTip"]*math.sin(math.radians(M2+M3))
    return round(x, 4), round(y, 4),round(z, 4)


data = {
    "legNames": [
        "front_right",
        "center_right",
        "rear_right",
        "rear_left",
        "center_left",
        "front_left"
    ],
    "legMountX": [
        60.0,
        120.0,
        60.0,
        -60.0,
        -120.0,
        -60.0
    ],
    "legMountY": [
        103.923,
        0.0,
        -103.923,
        -103.923,
        0.0,
        103.923
    ],
    "legMountAngle": [
        60.0,
        0.0,
        -60.0,
        -120.0,
        -180.0,
        -240.0
    ],
    "legScale": [
        [1, -1, -1],
        [1, 1, 1],
        [1, -1, -1],
        [1, 1, 1],
        [1, -1, -1],
        [1, 1, 1]
    ],
    "legJoint1ToJoint2": 40.0,
    "legJoint2ToJoint3": 120.0,
    "legJoint3ToTip": 160.0,

    "step_length": 160,
    "step_curviture_distance": 0,
    "step_height": 80
}
ser = serial.Serial("COM13", 1000000, timeout=1)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = []
y = []
z = []
while True:
    angles = read_pos()
    for leg in range(int(len(angles) / 3)):
        temp = angels_to_coord(angles[leg * 3], angles[leg * 3 + 1], angles[leg * 3 + 2], leg)
        x.append(temp[0])
        y.append(temp[1])
        z.append(temp[2])
    ax.scatter(x, y, z)
    plt.draw()
    plt.pause(1)
    ax.cla()
    x = []
    y = []
    z = []