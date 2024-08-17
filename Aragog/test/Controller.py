import pygame
import math

# Initialisiere pygame und den PS4 Controller
pygame.init()
pygame.joystick.init()

# Versuche, den ersten angeschlossenen Joystick (Controller) zu initialisieren
try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("PS4 Controller verbunden")
except pygame.error:
    print("Kein Controller gefunden.")
    exit()

# Zuordnung von Button IDs zu Namen
button_mapping = {
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

# Prüfe, ob der Controller Hat-Schalter hat
num_hats = joystick.get_numhats()

# Endlosschleife, um die Joystick-Positionen und gedrückten Tasten zu überwachen
try:
    while True:
        pygame.event.pump()  # Ereignisse abfragen, um den Joystick-Status zu aktualisieren

        if math.sqrt(round(joystick.get_axis(0), 2)**2+round(joystick.get_axis(1), 2)**2) > 0.2:
            print(f"Joystick L: {round(joystick.get_axis(0), 2)}, {round(joystick.get_axis(1), 2)}")
            if round(joystick.get_axis(0), 2) > 0:
                print(f"Angle L: {math.degrees(math.atan(round(joystick.get_axis(1), 2)/round(joystick.get_axis(0), 2)))+90}")
            elif round(joystick.get_axis(0), 2) < 0:
                print(f"Angle L: {math.degrees(math.atan(round(joystick.get_axis(1), 2)/round(joystick.get_axis(0), 2)))+270}")
            else:
                if round(joystick.get_axis(1), 2) >= 0:
                    print(f"Angle L: 180")
                else:
                    print(f"Angle L: 0")

        if math.sqrt(round(joystick.get_axis(2), 2) ** 2 + round(joystick.get_axis(3), 2) ** 2) > 0.2:
            print(f"Joystick R: {round(joystick.get_axis(2), 2)}, {round(joystick.get_axis(3), 2)}")
            if round(joystick.get_axis(2), 2) > 0:
                print(f"Angle R: {math.degrees(math.atan(round(joystick.get_axis(3), 2)/round(joystick.get_axis(2), 2)))+270}")
            elif round(joystick.get_axis(2), 2) < 0:
                print(f"Angle R: {math.degrees(math.atan(round(joystick.get_axis(3), 2)/round(joystick.get_axis(2), 2)))+90}")
            else:
                if round(joystick.get_axis(3), 2) >= 0:
                    print(f"Angle R: 0")
                else:
                    print(f"Angle R: 180")


        print(f"L: {round(joystick.get_axis(4), 2)}")
        print(f"R: {round(joystick.get_axis(5), 2)}")

        # Ausgabe der gedrückten Tasten
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i):
                print(f"Button {button_mapping.get(i, 'Unknown')}: Pressed")

        print("---")  # Trennlinie für eine klarere Ausgabe

        pygame.time.wait(10)  # Warte 100ms bevor die nächste Abfrage erfolgt
except KeyboardInterrupt:
    print("Programm beendet")
finally:
    pygame.quit()
