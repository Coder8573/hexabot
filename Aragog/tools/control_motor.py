import time

import serial
import serial.tools.list_ports


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return (~checksum) & 0xFF


def calc_low_byte(data):
    return data & 0xFF


def calc_high_byte(data):
    return (data >> 8) & 0xFF

def move(serial, motor, steps):
    #steps = int(round(angle*2048, 0))
    packet = [0xFF, 0xFF, motor, 0x07, 0x03, 0x2A, calc_low_byte(steps), calc_high_byte(steps)]
    packet.append(calculate_checksum(packet))
    print(packet)
    serial.write(bytearray(packet))


def disable_force(serial, ID):
    print("disable force")
    packet = [0xFF, 0xFF, ID, 0x04, 0x03, 0x28, 0]
    packet.append(calculate_checksum(packet[2:]))
    packet = bytearray(packet)
    serial.write(packet)

def enable_force(serial, ID):
    print("enable force")
    packet = [0xFF, 0xFF, ID, 0x04, 0x03, 0x28, 1]
    packet.append(calculate_checksum(packet[2:]))
    serial.write(bytearray(packet))

ports = serial.tools.list_ports.comports()

for i in range(len(ports)):
    print(f"{i}: Name: {ports[i].device} | Beschreibung: {ports[i].description}")

port = str(ports[int(input("Gib einen Port an: "))].device)
#port = "/dev/ttyACM0"
#motor = int(input("Gib einen Motor an: "))
#angle = float(input("Gib einen Winkel an: "))
steps = int(input("steps: "))
serial = serial.Serial(port, 1000000, timeout=1)
enable_force(serial, 254)
time.sleep(1)
move(serial, 254, steps)

time.sleep(5)
disable_force(serial, 254)
time.sleep(2)