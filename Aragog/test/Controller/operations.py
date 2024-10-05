import math


#def max(val, min, max):
#    if val < min:
#        return min
#    elif val > max:
#        return max
#    else:
#        return val

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def map_value(val, in_min, in_max, out_min, out_max):
    return ((val-in_min)/(in_max-in_min))*(out_max-out_min)+out_min


def lerp(val1, val2, t):
    return val1 * (1.0 - t) + (val2 * t)


def calc_hypotenuse(x, y):
    return math.sqrt(x**2+y**2)

