import serial
import time

class ST3215BusServo:
    def __init__(self, port, baudrate=1000000):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(1)  # Wartezeit für die serielle Verbindung

    def send_command(self, command):
        checksum = sum(command) & 0xFF
        command.append(checksum)
        self.ser.write(command)
        time.sleep(0.1)  # Wartezeit für die Verarbeitung

    def set_servo_position(self, servo_id, position):
        # ST3215 Servo Befehlsformat: [0x55, 0x55, ID, Länge, Befehl, Parameter...]
        command = [0x55, 0x55, servo_id, 0x07, 0x01, position & 0xFF, (position >> 8) & 0xFF, 0, 0]
        self.send_command(command)

    def close(self):
        self.ser.close()

#if __name__ == "__main__":
#    port = 'COM8'  # Beispielport, für Windows könnte es 'COM3' sein
#    servo = ST3215BusServo(port)
#
#    try:
#        servo_id = 4
#        position = 200  # Beispielposition, Bereich von 0 bis 1000 (abhängig von der Servospezifikation)
#        servo.set_servo_position(servo_id, position)
#        print("Befehl gesendet.")
#    finally:
#        servo.close()
#        print("Serielle Verbindung geschlossen.")

def read():
    string = ""
    while serial.in_waiting > 0:
        string = serial.readline().decode('utf-8').strip()
    return string


port = 'COM8'
serial = serial.Serial(port=port, baudrate=1000000, timeout=0.1)



#         Header     , ID  , Data Len, Status
command = [0x55, 0x55, 0x04,     0x07,   0x01]
checksum = sum(command) & 0xFF
command.append(checksum)
for i in command:
    serial.write(i)

time.sleep(1)

print(read())
