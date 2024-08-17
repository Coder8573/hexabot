packets = [[255, 255, 254, 132, 131, 42, 5, 7, 8, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 18, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 28, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 37, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 47, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 56, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 66, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 76, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 85, 5, 0, 0, 0, 0],

           [255, 255, 254, 132, 131, 42, 5, 7, 85, 5, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 103, 9, 0, 0, 0, 0],

           [255, 255, 254, 132, 131, 42, 5, 7, 118, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 128, 9, 0, 0, 0, 0],
           [255, 255, 254, 132, 131, 42, 5, 7, 132, 9, 0, 0, 0, 0]]

import serial
import time


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return (~checksum) & 0xFF


def send_packet(ser, packet):
    packet[3] = len(packet) - 1
    packet.append(calculate_checksum(packet))
    print(packet)
    packet = bytearray(packet)
    print(packet)

    ser.write(packet)
    time.sleep(0.2)

ser = serial.Serial('COM13', 1000000, timeout=1)


for i in packets:
    send_packet(ser, i)
    time.sleep(1)
ser.close()
