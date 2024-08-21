point = [[], [], [], [], [], []]
walk_progress = 0 # Range: 0 - 1
current_gait = 1
new_gait = 1

push_fraction = 0.5
speed_multiplier = 0.5
stride_length_multiplier = 1.5
lift_height_multiplier = 1.0
max_stride_length = 200
max_speed = 100

test_points = []

points = 0
def change_gait(gait):
    if gait == 0:
        push_fraction = 50

        speed_multiplier = (speed - 0.20) * 0.8 + 0.05
        stride_length_multiplier = 1
        lift_height_multiplier = 1.8
        max_stride_length = 230
        max_speed = 130


    elif gait == 1:
        push_fraction = 50

        speed_multiplier = (speed - 0.20) * 0.8 + 0.05
        stride_length_multiplier = 1
        lift_height_multiplier = 1.8
        max_stride_length = 230
        max_speed = 130

def gen_point(leg):
    pass
