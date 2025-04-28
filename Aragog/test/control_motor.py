import serial
import serial.tools.list_ports


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return (~checksum) & 0xFF


def calc_low_byte(data):
    return data & 0xFF


def calc_high_byte(data):
    return (data >> 8) & 0xFF

def move(serial, motor, angle):
    steps = int(round(angle*2048, 0))
    packet = [0xFF, 0xFF, motor, 0x07, 0x03, 0x2A, calc_low_byte(steps[0]), calc_high_byte(steps[0])]
    packet.append(calculate_checksum(packet))
    serial.write(bytearray(packet))

ports = serial.tools.list_ports.comports()

for port in ports:
    print(f"Name: {port.device} | Beschreibung: {port.description}")

#port = input("Gib einen Port an: ")
port = "/dev/ttyAMA10"
motor = int(input("Gib einen Motor an: "))
angle = float(input("Gib einen Winkel an: "))
serial = serial.Serial(port, 1000000, timeout=1)
move(serial, motor, angle)
