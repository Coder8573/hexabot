import time

import serial


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return (~checksum) & 0xFF


def build_packet(id, instruction, parameters):
    packet = [0xFF, 0xFF, id, len(parameters) + 2, instruction] + parameters
    checksum = calculate_checksum(packet[2:])
    packet.append(checksum)
    print(packet)
    return bytearray(packet)


def send_packet(ser, packet):
    ser.write(packet)


def receive_response(ser):
    response = ser.read_until(expected=b'\xFF\xFF')
    if len(response) < 4:
        return None
    data_length = response[3]
    response += ser.read(data_length + 1)
    return response


def set_servo_position(ser, servo_id, position):
    # Position should be between 0 and 4095
    position_low_byte = position & 0xFF
    position_high_byte = (position >> 8) & 0xFF


    instruction = 0x03  # WRITE DATA instruction
    parameters = [0x2A, position_low_byte, position_high_byte, 0x00, 0x00, 1, 150]  # Position, time, speed
    packet = build_packet(servo_id, instruction, parameters)
    send_packet(ser, packet)
    #response = receive_response(ser)
    #return response


def main():
    # Serial port configuration (adjust as needed)
    ser = serial.Serial('COM13', 1000000, timeout=1)

    servo_id = 254  # Example servo ID
    position = 2048  # Example position

    set_servo_position(ser, servo_id, 2048)
    #set_servo_position(ser, servo_id, 1792)
    #time.sleep(1)
#
    #set_servo_position(ser, servo_id, 2304)
    #time.sleep(2)
#
    #set_servo_position(ser, servo_id, 2048)

    #response = set_servo_position(ser, servo_id, 512)
    #print("Response:", response)
    #time.sleep(1.2)
#
    #response = set_servo_position(ser, servo_id, 3914)
    #print("Response:", response)
    #time.sleep(0.8)
#
    #response = set_servo_position(ser, servo_id, 2048)
    #print("Response:", response)

    ser.close()


if __name__ == "__main__":
    main()
