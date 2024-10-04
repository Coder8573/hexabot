import pygame
import math
import operations


class controller():
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joy_l_pos = [0, 0]
        self.joy_r_por = [0, 0]
        self.joy_l_smoothing = 0.012
        self.joy_r_smoothing = 0.012
        self.mapping = {
            0: "Cross",
            1: "Circle",
            2: "Square",
            3: "Triangle",
            4: "Share",
            5: "PS",
            6: "Option",
            7: "Left_Joystick",
            8: "Right_Joystick",
            9: "L1",
            10: "R1",
            11: "up",
            12: "down",
            13: "left",
            14: "right",
            15: "touch"
        }
        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print("PS4 Controller verbunden")
        except pygame.error:
            print("Kein Controller gefunden.")
            exit()

    def get_mapping(self):
        return self.mapping

    def Joystick_L(self):
        pygame.event.pump()  # Ereignisse abfragen, um den Joystick-Status zu aktualisieren
        x = round(self.joystick.get_axis(0), 2)
        y = round(self.joystick.get_axis(1), 2)
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
            return {"dir": dir, "speed": speed, "x": self.joy_l_pos[0], "y": self.joy_l_pos[1], "vector": self.joy_l_pos, "vector_raw": [x, y]}

    def Joystick_R(self):
        pygame.event.pump()  # Ereignisse abfragen, um den Joystick-Status zu aktualisieren
        x = round(self.joystick.get_axis(2), 2)
        y = round(self.joystick.get_axis(3), 2)
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
            return {"dir": dir, "speed": speed, "x": self.joy_r_por[0], "y": self.joy_r_por[1], "vector": self.joy_r_por, "vector_raw": [x, y]}

    def Trigger_L(self):
        #print(f"L: {round(joystick.get_axis(4), 2)}")
        return round(self.joystick.get_axis(4), 2)

    def Trigger_R(self):
        #print(f"R: {round(joystick.get_axis(5), 2)}")
        return round(self.joystick.get_axis(5), 2)

    def get_pressed_buttons(self, button=None):
        pygame.event.pump()
        if button is None:
            pressed_buttons = []
            for i in range(len(self.mapping)):
                if self.joystick.get_button(i):
                    #print(f"Button {self.mapping.get(i, 'Unknown')}: Pressed")
                    pressed_buttons.append(i)
            return pressed_buttons
        else:
            return self.joystick.get_button(button)
