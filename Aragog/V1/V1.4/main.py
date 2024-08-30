import time

from control import control
from controller import controller

control = control("COM13")
controller = controller()
#control.plot_walk()

try:
    #time.sleep(1)
    control.home()
    #time.sleep(2)
    while True:
    #for i in range(len(control.walk_points)):
        Joystick_L = controller.Joystick_L()
        #print(Joystick_L)
        if Joystick_L != None:
            control.walk(Joystick_L["dir"], Joystick_L["speed"], method=0)# Joystick_L["dir"]
        time.sleep(0.02)
        #time.sleep(0.1)
    #time.sleep(0.5)

    control.disable_force(254)
    control.close()

# time.sleep(1)
# control.pre_move_local_coord(1, [150, 0, -80])
# control.pre_move_local_coord(3, [150, 0, -80])
# control.pre_move_local_coord(4, [150, 0, -80])
# control.pre_move_local_coord(6, [150, 0, -80])
# control.execute_move()
#
# time.sleep(1)
# control.pre_move(1, [270, 103.923, -80])
# control.pre_move(3, [270, -103.923, -80])
# control.pre_move(4, [-270, -103.923, -80])
# control.pre_move(6, [-210, 103.923, -80])
# control.execute_move()
#
# time.sleep(1)
# control.pre_move(1, [270, 103.923, -160])
# control.pre_move(3, [270, -103.923, -160])
# control.pre_move(4, [-270, -103.923, -160])
# control.pre_move(6, [-270, 103.923, -160])
# control.execute_move()

except KeyboardInterrupt:
    control.disable_force(254)
    control.close()
