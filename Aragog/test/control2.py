import time
import serial

import calc

ser = serial.Serial('COM8', 1000000, timeout=1)

packet = []
#def execute_move():
#    packet = [0xFF, 0xFF, 0xFE, 0x02, 0x05]
#    packet.append(calculate_checksum(packet[2:]))
#    ser.write(bytearray(packet))
#
#
#def pre_move(leg, x, y, z):
#    steps = calc.calc_steps([x, y, z], leg)
#    #print(steps)
#    for i in range(len(steps)):
#        ID = ((leg*3)-2)+i
#        position = steps[i]
#        position_low_byte = position & 0xFF
#        position_high_byte = (position >> 8) & 0xFF
#        packet = [0xFF, 0xFF, ID, 0x09, 0x04, 0x2A, position_low_byte, position_high_byte, 0, 0]
#        packet.append(calculate_checksum(packet))
#        #print(packet)
#        ser.write(bytearray(packet))
#        time.sleep(0.0000002)

def calc_low_byte(data):
    return data & 0xFF

def calc_high_byte(data):
    return (data >> 8) & 0xFF

def move(leg, x, y, z):#, directon, speed, rotation
    steps = calc.calc_steps([x, y, z], leg)
    if(packet == []):
        print(steps)
    #for i in range(27, 29):
    #packet = [0xFF, 0xFF, 0xFE, i, 0x83, 0x2A, calc_low_byte(steps[0]), calc_high_byte(steps[0])]
    packet = [0xFF, 0xFF, 0xFE, 27, 0x83, 0x2A, 0x06, (leg*3)-2, calc_low_byte(steps[0]), calc_high_byte(steps[0]), 0X00, 0X00, 0x00, 0X00
              , (leg*3)-1, calc_low_byte(steps[1]), calc_high_byte(steps[1]), 0X00, 0X00, 0x00, 0X00
              , (leg*3), calc_low_byte(steps[2]), calc_high_byte(steps[2]), 0X00, 0X00, 0x00, 0X00]
    #print(packet)
    packet.append(calculate_checksum(packet))
    ser.write(bytearray(packet))
    #time.sleep(0.05)
    #time.sleep(2)

    #packet = [0xFF, 0xFF, 0xFE, 27, 0x83, 0x2A, 0x06, (leg*3)-2, 0x08, 0X00, 0X00, 0X00, 0x00, 0X00
    #          , (leg*3)-1, 0x08, 0X00, 0X00, 0X00, 0x00, 0X00
    #          , (leg*3), 0x08, 0X00, 0X00, 0X00, 0x00, 0X00]
    #print(packet)
    #packet.append(calculate_checksum(packet))
    #ser.write(bytearray(packet))
    #print(steps)
    #for i in range(len(steps)):
    #    ID = ((leg*3)-2)+i
    #    position = steps[i]
    #    position_low_byte = position & 0xFF
    #    position_high_byte = (position >> 8) & 0xFF
    #    packet = [0xFF, 0xFF, ID, 0x07, 0x03, 0x2A, position_low_byte, position_high_byte]
    #    packet.append(calculate_checksum(packet))
    #    ser.write(bytearray(packet))
        #print(packet)
        #time.sleep(0.0000002)

    #ID = 3
    #position = steps[2]
    #position_low_byte = position & 0xFF
    #position_high_byte = (position >> 8) & 0xFF
    #packet = [0xFF, 0xFF, ID, 0x07, 0x03, 0x2A, position_low_byte, position_high_byte]
    #packet.append(calculate_checksum(packet))
    #ser.write(bytearray(packet))
    #print(packet)

#[180, 180, 90]


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return (~checksum) & 0xFF


def disable_force(ID):
    packet = [0xFF, 0xFF, ID, 0x04, 0x03, 0x28, 0]
    packet.append(calculate_checksum(packet[2:]))
    #print(packet)
    packet = bytearray(packet)
    #print(packet)
    ser.write(packet)

def home():
    steps = [2048, 1024, 2048]
    # for i in range(27, 29):
    # packet = [0xFF, 0xFF, 0xFE, i, 0x83, 0x2A, calc_low_byte(steps[0]), calc_high_byte(steps[0])]
    for leg in range(1, 7):
        if (leg % 2 == 0):
            packet = [0xFF, 0xFF, 0xFE, 27, 0x83, 0x2A, 0x06, (leg * 3) - 2, calc_low_byte(steps[0]), calc_high_byte(steps[0]),
                      0X00, 0X00, 0x00, 0X00
                , (leg * 3) - 1, calc_low_byte(4096-steps[1]), calc_high_byte(4096-steps[1]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3), calc_low_byte(4096-steps[2]), calc_high_byte(4096-steps[2]), 0X00, 0X00, 0x00, 0X00]
        else:
            packet = [0xFF, 0xFF, 0xFE, 27, 0x83, 0x2A, 0x06, (leg * 3) - 2, calc_low_byte(steps[0]), calc_high_byte(steps[0]),
                      0X00, 0X00, 0x00, 0X00
                , (leg * 3) - 1, calc_low_byte(steps[1]), calc_high_byte(steps[1]), 0X00, 0X00, 0x00, 0X00
                , (leg * 3), calc_low_byte(steps[2]), calc_high_byte(steps[2]), 0X00, 0X00, 0x00, 0X00]
        print(packet)
        packet.append(calculate_checksum(packet))
        ser.write(bytearray(packet))
    execute_move()
    #steps = [2048, 2048, 2048]
    #for i in range(20, 50):
    #    packet = [0xFF, 0xFF, 0xFE, i, 0x83, 0x2A, 0x06]
    #    for i in range(1, 6):
    #        for j in range(0, 3):
    #            for k in [(i*3)-2+j, calc_low_byte(steps[j]), calc_high_byte(steps[j]), 0X00, 0X00, 0x00, 0X00]:
    #                packet.append(k)
    ## print(packet)
    #    packet.append(calculate_checksum(packet))
    #    print(packet)
    #    ser.write(bytearray(packet))
    #    time.sleep(1)
#disable_force(1)
#move(1, 160, 0, 20)
#move(2, 160, 0, 20)
#move(3, 160, 0, 20)
#execute_move()
#time.sleep(1)
#move(1, 160, 0, -40)
#move(2, 160, 0, -40)
#move(3, 160, 0, -40)
#execute_move()
#time.sleep(3)
#disable_force(254)
