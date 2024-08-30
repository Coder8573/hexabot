import serial
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

ser = serial.Serial('COM8', 1000000, timeout=1)
old_ID = 2
new_ID = 4
packet = [0xFF, 0xFF, old_ID, 0x04, 0x03, 0x37, 0x00]
send_packet(ser, packet)
packet = [0xFF, 0xFF, old_ID, 0x04, 0x03, 0x5, new_ID]
send_packet(ser, packet)
packet = [0xFF, 0xFF, new_ID, 0x04, 0x03, 0x37, 0x01]
send_packet(ser, packet)

#packet = [255, 255, 1, 11, 3, 42, 0, 0]
#send_packet(ser, packet)
#position = 1000
#position_low_byte = position & 0xFF
#position_high_byte = (position >> 8) & 0xFF
#packet = [0xFF, 0xFF, 0xFE, 5, 0x03, 0x2A, position_low_byte, position_high_byte]
#send_packet(ser, packet)
#ser.write([0xFF, 0xFF, 0x01, 6, 0x03, 0x2A, position_low_byte, position_high_byte])
ser.close()