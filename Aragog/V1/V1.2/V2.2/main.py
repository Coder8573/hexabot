import time

from control import control
from controller import controller

control = control("COM13")
controller = controller()
gait = 1

try:
    control.home((180, 0, -80))
    while True:
    #for i in range(len(control.walk_points)):
        Joystick_L = controller.Joystick_L()
        Joystick_R = controller.Joystick_R()
        L1 = controller.get_pressed_buttons(9)
        R1 = controller.get_pressed_buttons(10)
        Triangle = controller.get_pressed_buttons(3)
        Square = controller.get_pressed_buttons(2)
        if L1 or R1:
            gait = gait + R1 - L1
            if gait > 5:
                gait = 0
            if gait < 0:
                gait = 5
            print(f"gait: {gait}")
            while L1 or R1:
                L1 = controller.get_pressed_buttons(9)
                R1 = controller.get_pressed_buttons(10)
        if Triangle:
            control.walk_to_home_pos()
            print(f"gait: {gait}")
            while Triangle:
                Triangle = controller.get_pressed_buttons(3)
        if Square:
            control.home(coord=(180, 0, -80))
            print(f"gait: {gait}")
            while Square:
                Square = controller.get_pressed_buttons(2)

        pressed_buttons = controller.get_pressed_buttons()
        #print(Joystick_L)
        if Joystick_L != None and Joystick_R != None:
            control.walk(Joystick_L["dir"], Joystick_L["speed"], Joystick_R["speed"], Joystick_R["dir"], gait=gait, origin_point=(180, 0, -80))# Joystick_L["dir"]
            # control.walk_to_home_pos()
        if Joystick_L != None and Joystick_R == None:
            control.walk(Joystick_L["dir"], Joystick_L["speed"], 0, 0, gait=gait, origin_point=(180, 0, -80))  # Joystick_L["dir"]

        if Joystick_R != None and Joystick_L == None:
            control.turn(Joystick_R["dir"], Joystick_R["speed"], (180, 0, -80))
        #control.rotate()
        time.sleep(0.01)
        #time.sleep(0.1)
    #time.sleep(0.5)

    control.disable_force(254)
    control.close()


except KeyboardInterrupt:
    control.disable_force(254)
    control.close()
