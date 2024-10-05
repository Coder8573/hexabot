import time

from controller import controller
import system_check

if system_check.operating_system == "Windows":
    controller = controller(system_check.operating_system)

elif system_check.operating_system == "Linux":
    controller = controller(system_check.operating_system)

else:
    quit("Operating system not supported")

while True:
    Joystick_L = controller.Joystick_L()
    Joystick_R = controller.Joystick_R()
    print(f"Joystick_L: {Joystick_L}, Joystick_R: {Joystick_R}")
    #L2 = controller.Trigger_L()
    #R2 = controller.Trigger_R()
    #print(f"L2: {L2}, R2: {R2}")
    #L1 = controller.get_pressed_buttons("L1")
    #R1 = controller.get_pressed_buttons("R1")
    #Circle = controller.get_pressed_buttons("Circle")
    #Triangle = controller.get_pressed_buttons("Triangle")
