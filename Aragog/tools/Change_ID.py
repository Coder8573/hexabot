import serial
import serial.tools.list_ports
import time


def receive_response(ser):
    response = ser.read_until(expected=b'\xFF\xFF')
    if len(response) < 4:
        return None
    data_length = response[3]
    response += ser.read(data_length + 1)
    return response

def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return (~checksum) & 0xFF
def send_packet(ser, packet):
    checksum = calculate_checksum(packet[2:])
    packet.append(checksum)

    print(packet)
    packet = bytearray(packet)
    print(packet)

    ser.write(packet)
    time.sleep(0.2)
    response = receive_response(ser)
    print("Response:", response)


ports = serial.tools.list_ports.comports()

for i in range(len(ports)):
    print(f"{i}: Name: {ports[i].device} | Beschreibung: {ports[i].description}")

port = str(ports[int(input("Gib einen Port an: "))].device)
ser = serial.Serial(port, 1000000, timeout=1)
old_ID = int(input("Alte ID: "))
new_ID = int(input("Neue ID: "))
packet = [0xFF, 0xFF, old_ID, 0x04, 0x03, 0x37, 0x00]
send_packet(ser, packet)
packet = [0xFF, 0xFF, old_ID, 0x04, 0x03, 0x5, new_ID]
send_packet(ser, packet)
packet = [0xFF, 0xFF, new_ID, 0x04, 0x03, 0x37, 0x01]
send_packet(ser, packet)

ser.close()