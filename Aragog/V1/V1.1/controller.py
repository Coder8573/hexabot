import pygame
import math

class controller():
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
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
            return {"dir": dir, "speed": speed, "x": x, "y": y}

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
            return {"dir": dir, "speed": speed, "x": x, "y": y}

    def Trigger_L(self):
        #print(f"L: {round(joystick.get_axis(4), 2)}")
        return round(self.joystick.get_axis(4), 2)

    def Trigger_R(self):
        #print(f"R: {round(joystick.get_axis(5), 2)}")
        return round(self.joystick.get_axis(5), 2)

    def get_pressed_buttons(self):
        pressed_buttons = []
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                print(f"Button {self.mapping.get(i, 'Unknown')}: Pressed")
                pressed_buttons.append(i)
        return pressed_buttons




