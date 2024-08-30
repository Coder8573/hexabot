import pygame
import math
import operations


class controller():
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joy_l_pos = [0, 0]
        self.joy_r_por = [0, 0]
        self.joy_l_smoothing = 1
        self.joy_r_smoothing = 1
        self.mapping = {
            0: "Cross",
            1: "Circle",
            2: "Triangle",
            3: "Square",
            4: "L1",
            5: "R1",
            6: "L2",
            7: "R2",
            8: "Share",
            9: "Option",
            10: "PS",
            11: "Left_Joystick",
            12: "Right_Joystick"
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
            return {"dir": dir, "speed": speed, "x": self.joy_l_pos[0], "y": self.joy_l_pos[1], "vector": self.joy_l_pos}

    def Joystick_R(self):
        pygame.event.pump()  # Ereignisse abfragen, um den Joystick-Status zu aktualisieren
        x = round(self.joystick.get_axis(3), 2)
        y = round(self.joystick.get_axis(4), 2)
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
        return round(self.joystick.get_axis(2), 2)

    def Trigger_R(self):
        pygame.event.pump()
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

#con = controller()
#while 1:
#    print(con.Joystick_L(), con.Joystick_R())