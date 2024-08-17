import math

from scipy.integrate import quad
from scipy.optimize import newton

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import config


# Bezier Kurve erstellen
def bezier_curve(t, curve_boundary):
    P0, P1, P2 = curve_boundary
    x = (1-t)**2 * P0[0] + 2*(1-t) * t * P1[0] + t**2 * P2[0]
    y = (1-t)**2 * P0[1] + 2*(1-t) * t * P1[1] + t**2 * P2[1]
    return [x, y]


# Ableiten (derivation = Ableiten)
def bezier_curve_derivation(t, curve_boundary):
    P0, P1, P2 = curve_boundary
    x = 2*(1-t) * (P1[0] - P0[0]) + 2*t * (P2[0] - P1[0])
    y = 2*(1-t) * (P1[1] - P0[1]) + 2*t * (P2[1] - P1[1])
    return [x, y]


# Satz des Pytagoras
def pyt(v):
    # squrt(x**2 + y**2)
    return (v[0]**2 + v[1]**2)**0.5


# Gesamtlänge der Kurve berechnen
def curve_length(curve_boundary):
    integrand = lambda t: pyt(bezier_curve_derivation(t, curve_boundary))
    length = quad(integrand, 0, 1)[0]
    return length



# Längen-Funktion L(t)
def L_t(t, curve_boundary):
    integrand = lambda u: pyt(bezier_curve_derivation(u, curve_boundary))
    length = quad(integrand, 0, t)[0]
    return length


# Umkehrfunktion L^-1(s) finden
def inverse_L(s, curve_boundary, L):
    func = lambda t: L_t(t, curve_boundary) - s
    t_initial_guess = s / L
    t_solution = newton(func, t_initial_guess)
    return t_solution


def bezier_curve_3D(t, curve_boundary):
    P0, P1, P2 = curve_boundary
    x = (1-t)**2 * P0[0] + 2*(1-t) * t * P1[0] + t**2 * P2[0]
    y = (1-t)**2 * P0[1] + 2*(1-t) * t * P1[1] + t**2 * P2[1]
    z = (1-t)**2 * P0[2] + 2*(1-t) * t * P1[2] + t**2 * P2[2]
    return [x, y, z]

def bezier_curve_derivation_3D(t, curve_boundary):
    P0, P1, P2 = curve_boundary
    x = 2*(1-t) * (P1[0] - P0[0]) + 2*t * (P2[0] - P1[0])
    y = 2*(1-t) * (P1[1] - P0[1]) + 2*t * (P2[1] - P1[1])
    z = 2*(1-t) * (P1[2] - P0[2]) + 2*t * (P2[2] - P1[2])
    return [x, y, z]

def pyt_3D(v):
    return (v[0]**2 + v[1]**2 + v[2]**2)**0.5

# Gesamtlänge der Kurve berechnen
def curve_length_3D(curve_boundary):
    integrand = lambda t: pyt_3D(bezier_curve_derivation_3D(t, curve_boundary))
    length, _ = quad(integrand, 0, 1)
    return length


# Längen-Funktion L(t)
def L_t_3D(t, curve_boundary):
    integrand = lambda u: pyt_3D(bezier_curve_derivation_3D(t, curve_boundary))
    length, _ = quad(integrand, 0, t)
    return length

# Umkehrfunktion L^-1(s) finden
def inverse_L_3D(s, curve_boundary, L):
    func = lambda t: L_t_3D(t, curve_boundary) - s
    t_initial_guess = s / L
    t_solution = newton(func, t_initial_guess)
    return t_solution

def diff_between_two_points(point1, point2):
    if len(point1) == 2:
        return math.sqrt((point2[0]-point1[0])**2 +
                         (point2[1]-point1[1])**2)

    if len(point1) == 3:
        return math.sqrt((point2[0] - point1[0]) ** 2 +
                         (point2[1] - point1[1]) ** 2 +
                         (point2[2] - point1[2]) ** 2)


def gen_curve_point(leg, t, start_point, end_point=(180, 0, -100), height=120):
    dist_between_points = diff_between_two_points(start_point, end_point)
    curve_boundary = ((-dist_between_points, 0), (-dist_between_points*0.5, height), (0, 0, 0))
    t = map_value(t, 0, 1, 0, curve_top_len)
    t_i = inverse_L(t, (curve_boundary), curve_top_len)
    point = bezier_curve(t_i, curve_top_boundary)
    point = [0, point[0], point[1]]
    point = [math.sin(math.radians(config.data["legMountAngle"][leg - 1])) * point[1] + end_point[0],
             math.cos(math.radians(config.data["legMountAngle"][leg - 1])) * point[1] + end_point[1],
             point[2] + end_point[2]]
    return point

#def gen_home_curve_points(leg, start_point, end_point=(180, 0, -100), height=120):
#    dist_between_points = diff_between_two_points(start_point, end_point)
#    curve_boundary = ((-dist_between_points, 0), (-dist_between_points*0.5, height), (0, 0))
#    curve_len = curve_length(curve_boundary)
#    points = []
#    #points.append((0, -dist_between_points, 0))
#    #points.append((0, -dist_between_points*0.5, height))
#    #points.append((0, 0, 0))
#    for t in range(0, 101):
#        t = map_value(t, 0, 100, 0, curve_len)
#        t_i = inverse_L(t, (curve_boundary), curve_len)
#        temp_point = bezier_curve(t_i, curve_boundary)
#        #temp_point = [0, temp_point[0], temp_point[1]]
#        #points.append(temp_point)
#        points.append([math.sin(math.radians(config.data["legMountAngle"][leg - 1])) * temp_point[0] + end_point[0],
#                         math.cos(math.radians(config.data["legMountAngle"][leg - 1])) * temp_point[0] + end_point[1],
#                         temp_point[1] + end_point[2]])
#    return points

def gen_home_curve_point(leg, t, dir, start_point, end_point=(0, 0, 0), height=0):
    start_point = path_point_to_local_coord(leg, start_point, (180, 0, -80), dir)
    curve_boundary = (start_point, [(start_point[0]+end_point[0])/2, (start_point[1]+end_point[1])/2, height+((start_point[2]+end_point[2])/2)], end_point)
    curve_len = curve_length_3D(curve_boundary)
    #points.append((0, -dist_between_points, 0))
    #points.append((0, -dist_between_points*0.5, height))
    #points.append((0, 0, 0))

    #print(curve_len)
    t = map_value(t, 0, 100, 0, curve_len)
    t_i = inverse_L_3D(t, curve_boundary, curve_len)
    point = bezier_curve_3D(t_i, curve_boundary)
    #temp_point = [0, temp_point[0], temp_point[1]]
    #points.append(temp_point)
    #points = [temp_point[0]*math.cos(math.atan((start_point[1]-end_point[1])/(start_point[0]-end_point[0]))),
    #          temp_point[0]*math.sin(math.atan((start_point[1]-end_point[1])/(start_point[0]-end_point[0]))),
    #          temp_point[1]]
    return point

def gen_turn_point(t, origin_point):
    r = diff_between_two_points((0, 0), (origin_point[0], 0.5*step_length))
    d = step_length
    max_rad = math.acos((d**2-2*(r**2))/(-2*(r**2)))
    len = (r*math.pi*math.degrees(max_rad))/180
    point = (math.cos(t*max_rad-0.5*max_rad)*r, math.sin(t*max_rad-0.5*max_rad)*r, origin_point[2])
    return point

def gen_point(leg, walk_progress, ground_touching_prozentage, origin_point, dir):
    if walk_progress <= 0.5*ground_touching_prozentage:
        t = map_value(walk_progress, 0,  0.5*ground_touching_prozentage, 0, 0.5)
        walk_point = [0, -step_length * t, 0]
        turn_point = gen_turn_point(t, origin_point)


    elif 0.5*ground_touching_prozentage < walk_progress < 100-(0.5*ground_touching_prozentage):
        t = map_value(walk_progress, 0.5 * ground_touching_prozentage, 100 - (0.5*ground_touching_prozentage), 0, 1)
        t_i = inverse_L(curve_top_len*t, curve_top_boundary, curve_top_len)
        point = bezier_curve(t_i, curve_top_boundary)
        point = [math.sin(math.radians(config.data["legMountAngle"][leg - 1] + dir)) * point[0] + origin_point[0],
                 math.cos(math.radians(config.data["legMountAngle"][leg - 1] + dir)) * point[0] + origin_point[1],
                 point[1] + origin_point[2]]

    elif walk_progress >= 100-(0.5*ground_touching_prozentage):
        t = map_value(walk_progress, 100-(0.5*ground_touching_prozentage), 100, 0, 0.5)
        walk_point = [0, 0.5*step_length-step_length * t, 0]
        turn_point = gen_turn_point(t+0.5, origin_point)

    else:
        exit("Error: walk_progress out of range")

    return point


def gen_next_path_point(leg, stepsize, walk_progress, ground_touching_prozentage, origin_point, dir):
    walk_progress = walk_progress + stepsize
    if walk_progress > 100:
        walk_progress = walk_progress % 100

    #print(f"walk progress: {walk_progress}")
    point = gen_point(leg, walk_progress, ground_touching_prozentage, origin_point, dir)
    return point, walk_progress

#def gen_whole_foot_path(ground_touching_prozentage, stepsize):
#    points = []
#    for i in range(0, 100+stepsize, stepsize):
#        points.append(path_point_to_local_coord(1, gen_point(i, ground_touching_prozentage, [160, 0, -160]), [160, 0, -160]))
#    return points

def path_point_to_local_coord(leg, point, origin_point, dir):
    point = [math.sin(math.radians(config.data["legMountAngle"][leg-1]+dir))*point[1]+origin_point[0],
             math.cos(math.radians(config.data["legMountAngle"][leg-1]+dir))*point[1]+origin_point[1],
             point[2]+origin_point[2]]
    return point

def map_value(val, old_min, old_max, new_min, new_max):
    return ((val-old_min)/(old_max-old_min))*(new_max-new_min)+new_min

def plot_3d_points(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Entpacken der Punkte in separate Listen für x, y und z
    x_vals = [point[0] for point in points]
    y_vals = [point[1] for point in points]
    z_vals = [point[2] for point in points]

    # Scatter plot der Punkte
    ax.scatter(x_vals, y_vals, z_vals)

    # Achsenbeschriftungen
    ax.set_xlabel('X Achse')
    ax.set_ylabel('Y Achse')
    ax.set_zlabel('Z Achse')

    # Titel setzen
    ax.set_title('3D Punkte Plot')

    # Bestimmen der gleichen Grenzen für alle Achsen
    max_range = max(max(x_vals) - min(x_vals), max(y_vals) - min(y_vals), max(z_vals) - min(z_vals))

    # Mittelpunkt der Achsen
    mid_x = (max(x_vals) + min(x_vals)) * 0.5
    mid_y = (max(y_vals) + min(y_vals)) * 0.5
    mid_z = (max(z_vals) + min(z_vals)) * 0.5

    # Setzen der gleichen Grenzen für alle Achsen
    ax.set_xlim(mid_x - max_range * 0.5, mid_x + max_range * 0.5)
    ax.set_ylim(mid_y - max_range * 0.5, mid_y + max_range * 0.5)
    ax.set_zlim(mid_z - max_range * 0.5, mid_z + max_range * 0.5)

    # Zeige den Plot an
    plt.show()


step_length = config.data["step_length"]
step_height = config.data["step_height"]

# Beispiel für eine quadratische Bézier-Kurve
curve_top_boundary = [[-0.5 * step_length, 0],
                      [0, step_height],
                      [0.5 * step_length, 0]]

line_bottom_left_boundary = [[0.5 * step_length, 0], [0, 0]]
line_bottom_right_boundary = [[0, 0], [-0.5 * step_length, 0]]

curve_top_len = curve_length(curve_top_boundary)
curve_bottom_right_len = 0.5 * step_length
curve_bottom_left_len = 0.5 * step_length

