import math


def max(val, min, max):
    if val < min:
        return min
    elif val > max:
        return max
    else:
        return val


def map_value(val, in_min, in_max, new_min, new_max):
    return ((val-in_min)/(in_max-in_min))*(new_max-new_min)+new_min


def lerp(val1, val2, t):
    return val1 * (1.0 - t) + (val2 * t)


def calc_hypotenuse(x, y):
    return math.sqrt(x**2+y**2)

