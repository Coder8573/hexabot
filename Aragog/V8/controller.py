import pygame
import math

import operations


class controller():
    def __init__(self, operating_system):
        pygame.init()
        pygame.joystick.init()
        self.joy_l_pos = [0, 0]
        self.joy_r_por = [0, 0]
        self.joy_l_smoothing = 1
        self.joy_r_smoothing = 1
        if operating_system == "Windows":
            self.button_mapping = {
                "Cross": 0,
                "Circle": 1,
                "Square": 2,
                "Triangle": 3,
                "Share": 4,
                "PS": 5,
                "Option": 6,
                "Left_Joystick": 7,
                "Right_Joystick": 8,
                "L1": 9,
                "R1": 10
            }
            self.analog_mapping = {
                "Joy_Left_x": 0,
                "Joy_Left_y": 1,
                "Joy_Right_x": 2,
                "Joy_Right_y": 3,
                "Trigger_Left": 4,
                "Trigger_Right": 5
            }
        elif operating_system == "Linux":
            self.button_mapping = {
                "Cross": 0,
                "Circle": 1,
                "Square": 3,
                "Triangle": 2,
                "Share": 8,
                "PS": 10,
                "Option": 9,
                "Left_Joystick": 11,
                "Right_Joystick": 12,
                "L1": 4,
                "R1": 5,
                "1": 13,
                "2": 14,
                "3": 15,
                "4": 16
            }
            self.analog_mapping = {
                "Joy_Left_x": 0,
                "Joy_Left_y": 1,
                "Joy_Right_x": 3,
                "Joy_Right_y": 4,
                "Trigger_Left": 2,
                "Trigger_Right": 5
            }
        else:
            self.button_mapping = {}
            self.analog_mapping = {}

        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print("PS4 Controller verbunden")
        except pygame.error:
            print("Kein Controller gefunden.")
            exit()

    def Joystick_L(self):
        pygame.event.pump()
        x = round(self.joystick.get_axis(self.analog_mapping["Joy_Left_x"]), 2)
        y = round(self.joystick.get_axis(self.analog_mapping["Joy_Left_y"]), 2)
        if math.sqrt(x ** 2 + y ** 2) > 0.2:
            if x > 0:
                dir = math.degrees(math.atan(y / x)) + 90
            elif x < 0:
                dir = math.degrees(math.atan(y / x)) + 270
            else:
                if y >= 0:
                    dir = 180
                else:
                    dir = 0
            speed = math.sqrt(x ** 2 + y ** 2)
            #print(f"Angle L: {dir}; Joystick L: {x}, {y}")
            self.joy_l_pos = [operations.lerp(self.joy_l_pos[0], x, self.joy_l_smoothing), operations.lerp(self.joy_l_pos[1], y, self.joy_l_smoothing)]
            #self.joy_l_pos = [x,y]
            return {"dir": dir, "speed": speed, "x": self.joy_l_pos[0], "y": self.joy_l_pos[1], "vector": self.joy_l_pos}

    def Joystick_R(self):
        pygame.event.pump()  # Ereignisse abfragen, um den Joystick-Status zu aktualisieren
        x = round(self.joystick.get_axis(self.analog_mapping["Joy_Right_x"]), 2)
        y = round(self.joystick.get_axis(self.analog_mapping["Joy_Right_y"]), 2)
        if math.sqrt(x ** 2 + y ** 2) > 0.2:
            if x > 0:
                dir = math.degrees(math.atan(y / x)) + 90
            elif x < 0:
                dir = math.degrees(math.atan(y / x)) + 270
            else:
                if y >= 0:
                    dir = 180
                else:
                    dir = 0
            speed = math.sqrt(x ** 2 + y ** 2)
            # print(f"Angle L: {dir}; Joystick L: {x}, {y}")
            self.joy_r_por = [operations.lerp(self.joy_r_por[0], x, self.joy_r_smoothing), operations.lerp(self.joy_r_por[1], y, self.joy_r_smoothing)]
            #self.joy_r_pos = [x, y]
            return {"dir": dir, "speed": speed, "x": self.joy_r_por[0], "y": self.joy_r_por[1], "vector": self.joy_r_por}

    #not working
    def Trigger_L(self):
        pygame.event.pump()
        #print(f"L: {round(joystick.get_axis(4), 2)}")
        return round(self.joystick.get_axis(self.analog_mapping["Trigger_Left"]), 2)

    def Trigger_R(self):
        pygame.event.pump()
        #print(f"R: {round(joystick.get_axis(5), 2)}")
        return round(self.joystick.get_axis(self.analog_mapping["Trigger_Right"]), 2)

    def get_pressed_buttons(self, button=None):
        pygame.event.pump()
        #print(max(self.button_mapping, key=self.button_mapping.get))
        if button is None:
            pressed_buttons = []
            for i in range(self.button_mapping[max(self.button_mapping, key=self.button_mapping.get)]+1):
                if self.joystick.get_button(i):
                    #print(f"Button {self.mapping.get(i, 'Unknown')}: Pressed")
                    print(i)
                    try:
                        pressed_buttons.append({value:key for key, value in self.button_mapping.items()}[i])
                    except KeyError:
                        pass
            return pressed_buttons
        else:
            return self.joystick.get_button(self.button_mapping[button])

#con = controller()
#while 1:
#    print(con.Joystick_L(), con.Joystick_R())