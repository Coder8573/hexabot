import time

from control import Control
from controller import controller

control = Control("COM13")
controller = controller()
gait = 1
try:
    #control.test()
    control.home((180, 0, -120))
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
            print("reset")
            control.reset()
            while Triangle:
                Triangle = controller.get_pressed_buttons(3)

        if Square:
            print("draw")
            control.draw()
            while Square:
                Square = controller.get_pressed_buttons(2)

        pressed_buttons = controller.get_pressed_buttons()
        #print(Joystick_L)
        if Joystick_L != None and Joystick_R != None:
            control.walk(Joystick_L["vector"], Joystick_R["vector"], gait=gait)# Joystick_L["dir"]
            # control.walk_to_home_pos()
        elif Joystick_L != None and Joystick_R == None:
            control.walk(Joystick_L["vector"], [0, 0], gait=gait)  # Joystick_L["dir"]

        elif Joystick_R != None and Joystick_L == None:
            control.walk([0, 0], Joystick_R["vector"], gait=gait)
        #control.rotate()
        time.sleep(0.01)
        #time.sleep(0.1)
    #time.sleep(0.5)

    control.disable_force(254)
    control.close()


except KeyboardInterrupt:
    control.disable_force(254)
    control.close()
