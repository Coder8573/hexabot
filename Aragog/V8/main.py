import time

from control import Control
from controller import controller
import config
import system_check

if system_check.operating_system == "Windows":
    control = Control("COM13")
    controller = controller(system_check.operating_system)

elif system_check.operating_system == "Linux":
    control = Control("/dev/ttyACM0")
    controller = controller(system_check.operating_system)

else:
    quit("Operating system not supported")

gait = 0

try:
    control.home(config.data["origin_point"])
    while True:
        start = time.time()
        test_time = 0
        Joystick_L = controller.Joystick_L()
        Joystick_R = controller.Joystick_R()
        L2 = controller.Trigger_L()
        R2 = controller.Trigger_R()
        #print(f"L2: {L2}, R2: {R2}")
        L1 = controller.get_pressed_buttons("L1")
        R1 = controller.get_pressed_buttons("R1")
        Circle = controller.get_pressed_buttons("Circle")
        Triangle = controller.get_pressed_buttons("Triangle")
        #Square = controller.get_pressed_buttons(2)
        if L1 or R1:
            gait = gait + R1 - L1
            if gait > 6:
                gait = 0
            if gait < -2:
                gait = 0
            print(f"gait: {gait}")
            while L1 or R1:
                L1 = controller.get_pressed_buttons("L1")
                R1 = controller.get_pressed_buttons("R1")

        if Triangle:
            print("home")
            control.home(config.data["origin_point"])
            while Triangle:
                Triangle = controller.get_pressed_buttons("Triangle")

        if gait < 0:
            control.hover(Joystick_L["vector_raw"], Joystick_R["vector_raw"], L2, R2, gait)
        elif gait > 0:
            if Joystick_L["vector_raw"] != [0, 0] or Joystick_R["vector_raw"] != [0, 0]:
                control.walk(Joystick_L["vector"], Joystick_R["vector"], gait=gait)
        else:
            print(controller.get_inputs())

        test_time = time.time()
        while (start+0.01) > time.time():
            pass
        test_time = time.time() - test_time
        print(f"Cycle Time: {start-time.time()}, Test Time: {test_time}")


except KeyboardInterrupt:
    control.disable_force(254)
    control.close()
