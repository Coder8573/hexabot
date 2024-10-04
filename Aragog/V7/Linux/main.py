import time

from control import Control
from controller import controller
import config

cycle = 0
control = Control("/dev/ttyACM0")
controller = controller()
gait = 1
walk_mode = 0
try:
    #control.test()
    control.home(config.data["origin_point"])
    while True:
    #for i in range(len(control.walk_points)):
        cycle = cycle + 1
        start = time.time()
        Joystick_L = controller.Joystick_L()
        Joystick_R = controller.Joystick_R()
        L1 = controller.get_pressed_buttons(4)
        R1 = controller.get_pressed_buttons(5)
        #Circle = controller.get_pressed_buttons(1)
        #Triangle = controller.get_pressed_buttons(3)
        #Square = controller.get_pressed_buttons(2)
        if L1 or R1:
            gait = gait + R1 - L1
            if gait > 6:
                gait = 0
            if gait < 0:
                gait = 6
            print(f"gait: {gait}")
            while L1 or R1:
                L1 = controller.get_pressed_buttons(4)
                R1 = controller.get_pressed_buttons(5)

        #if Triangle:
        #    print("home")
        #    control.home(config.data["origin_point"])
        #    while Triangle:
        #        Triangle = controller.get_pressed_buttons(3)
#
        #if Square:
        #    print("draw")
        #    control.draw()
        #    while Square:
        #        Square = controller.get_pressed_buttons(3)

        #if Circle:
        #    walk_mode = walk_mode + Circle
        #    if walk_mode > 1:
        #        walk_mode = 0
        #        print("Walk Mode")
        #    if walk_mode < 0:
        #        walk_mode = 1
        #        print("Hover Mode")
        #    #print(f"gait: {walk_mode}")
        #    while Circle:
        #        Circle = controller.get_pressed_buttons(1)

        #pressed_buttons = controller.get_pressed_buttons()
        #print(Joystick_L)
        if Joystick_L != None and Joystick_R != None:
            control.walk(Joystick_L["vector"], Joystick_R["vector"], gait=gait)  # Joystick_L["dir"]
            # control.walk_to_home_pos()
        elif Joystick_L != None and Joystick_R == None:
            control.walk(Joystick_L["vector"], [0, 0], gait=gait)  # Joystick_L["dir"]

        elif Joystick_R != None and Joystick_L == None:
            control.walk([0, 0], Joystick_R["vector"], gait=gait)
        # control.rotate()
        # time.sleep(0.01)
        # time.sleep(0.1)
        print(time.time() - start)
        while (start + 0.005) > time.time():
            pass
    #time.sleep(0.5)

    control.disable_force(254)
    control.close()


except KeyboardInterrupt:
    control.disable_force(254)
    control.close()
