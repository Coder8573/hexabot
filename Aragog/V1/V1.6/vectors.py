import math


def to_string(point1):
    if len(point1) < 3:
        return f"({point1[0]} | {point1[1]})"
    else:
        return f"({point1[0]} | {point1[1]} | {point1[2]})"

def add_point(point1, point2):
    if len(point1) < 3:
        return [point1[0] + point2[0], point1[1] + point2[1]]
    else:
        return [point1[0] + point2[0], point1[1] + point2[1], point1[2] + point2[2]]

def subtract_point(point1, point2):
    if len(point1) < 3:
        return [point1[0] - point2[0], point1[1] - point2[1]]
    else:
        return [point1[0] - point2[0], point1[1] - point2[1], point1[2] - point2[2]]

def multi_with_val(point1, val):
    if len(point1) < 3:
        return [point1[0] * val, point1[1] * val]
    else:
        return [point1[0] * val, point1[1] * val, point1[2] * val]

def multi_with_point(point1, point2):
    if len(point1) < 3:
        return [point1[0] * point2[0], point1[1] * point2[1]]
    else:
        return [point1[0] * point2[0], point1[1] * point2[1], point1[2] * point2[2]]

def divide_with_val(point1, val):
    return [point1[0]/val, point1[1]/val, point1[2]/val]

def divide_with_point(point1, point2):
    return [point1[0]/point2[0], point1[1]/point2[1], point1[2]/point2[2]]

def rotate(point1, angle, pivot):
    if angle == 0:
        return point1

    rad = math.radians(angle)
    point1[0] = point1[0] - pivot[0]
    point1[1] = point1[1] - pivot[1]

    x_rotated = point1[0] * math.cos(rad) - point1[1] * math.sin(rad)
    y_rotated = point1[0] * math.sin(rad) + point1[1] * math.cos(rad)

    point1[0] = x_rotated + pivot[0]
    point1[1] = y_rotated + pivot[1]
    return point1

def length(point):
    return math.sqrt(point[0] ** 2 + point[1] ** 2)

def distance(point1, point2):
    return length(subtract_point(point1, point2))