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
    length, _ = quad(integrand, 0, 1)
    return length


# Längen-Funktion L(t)
def L_t(t, curve_boundary):
    integrand = lambda u: pyt(bezier_curve_derivation(u, curve_boundary))
    length, _ = quad(integrand, 0, t)
    return length

# Umkehrfunktion L^-1(s) finden
def inverse_L(s, curve_boundary, L):
    func = lambda t: L_t(t, curve_boundary) - s
    t_initial_guess = s / L
    t_solution = newton(func, t_initial_guess)
    return t_solution

def gen_points(num_of_points, curve_len, curve_boundary):
    points = []
    if len(curve_boundary) == 3:
        for i in range(num_of_points):
            s_i = i * curve_len / (num_of_points - 1)
            t_i = inverse_L(s_i, curve_boundary, curve_len)
            points.append(bezier_curve(t_i, curve_boundary))

    elif len(curve_boundary) == 2:
        for i in range(num_of_points):
            points.append([curve_boundary[0][0] - (i * curve_len / (num_of_points - 1)), curve_boundary[0][1]])
        #print(points)
    return points

def gen_foot_path():
    step_length = config.data["step_length"]
    step_curviture_distance = config.data["step_curviture_distance"]
    step_height = config.data["step_height"]

    # Beispiel für eine quadratische Bézier-Kurve
    curve_left_boundary = [[-0.5*step_length, 0],
                          [-0.5*step_length - step_curviture_distance, 0],
                          [-0.5*step_length, (-step_length*step_height)/(step_length + 2*step_curviture_distance) + step_height]]

    curve_top_boundary = [[-0.5*step_length, (-step_length*step_height)/(step_length + 2*step_curviture_distance) + step_height],
                           [0, step_height],
                           [0.5*step_length, (-step_length*step_height)/(step_length + 2*step_curviture_distance) + step_height]]

    curve_right_boundary = [[0.5*step_length, (-step_length*step_height)/(step_length + 2*step_curviture_distance) + step_height],
                             [0.5*step_length + step_curviture_distance, 0],
                             [0.5*step_length, 0]]

    line_bottom_left_boundary = [[0.5*step_length, 0], [0, 0]]
    line_bottom_right_boundary = [[0, 0], [-0.5 * step_length, 0]]


    curve_top_len = curve_length(curve_top_boundary)
    curve_left_len = curve_length(curve_left_boundary)
    curve_right_len = curve_length(curve_right_boundary)
    curve_bottom_right_len = 0.5 * step_length
    curve_bottom_left_len = 0.5 * step_length

    points = []
    speed = 2
    top_length = curve_top_len + curve_left_len + curve_right_len
    bottom_length = step_length

    #print(top_length)
    #print(bottom_length)
    points.extend(gen_points(int(round(curve_bottom_right_len/speed, 0)), curve_bottom_right_len, line_bottom_right_boundary)[0:])
    points.extend(gen_points(int(round((curve_left_len/(top_length/bottom_length))/speed, 0)), curve_left_len, curve_left_boundary)[0:])
    points.extend(gen_points(int(round((curve_top_len/(top_length/bottom_length))/speed, 0)), curve_top_len, curve_top_boundary)[0:])
    points.extend(gen_points(int(round((curve_right_len/(top_length/bottom_length))/speed, 0)), curve_right_len, curve_right_boundary)[0:])
    points.extend(gen_points(int(round(curve_bottom_left_len/speed, 0)), curve_bottom_left_len, line_bottom_left_boundary)[0:])
    return points

def gen_next_point(leg, dir, origin_point, id_of_point, list_of_pints):
    point = list_of_pints[id_of_point]
    point = [math.sin(math.radians(dir))*point[0], math.cos(math.radians(dir))*point[0], point[1]]
    if origin_point[0] > 0:
        displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1])+math.atan(origin_point[1]/origin_point[0]))*math.sqrt(origin_point[0]**2+origin_point[1]**2) + config.data["legMountX"][leg-1],
                              math.sin(math.radians(config.data["legMountAngle"][leg-1])+math.atan(origin_point[1]/origin_point[0]))*math.sqrt(origin_point[0]**2+origin_point[1]**2) + config.data["legMountY"][leg-1],
                              origin_point[2]]
    elif origin_point[0] < 0:
        displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1])+math.atan(origin_point[1]/origin_point[0])+0.5*math.pi)*math.sqrt(origin_point[0]**2+origin_point[1]**2) + config.data["legMountX"][leg-1],
                              math.sin(math.radians(config.data["legMountAngle"][leg-1])+math.atan(origin_point[1]/origin_point[0])+0.5*math.pi)*math.sqrt(origin_point[0]**2+origin_point[1]**2) + config.data["legMountY"][leg-1],
                              origin_point[2]]
    else:
        displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1]))*origin_point[1] + config.data["legMountX"][leg-1],
                              math.sin(math.radians(config.data["legMountAngle"][leg-1]))*origin_point[1] + config.data["legMountY"][leg-1],
                              origin_point[2]]
    point = [point[0] + displacement_point[0], point[1] + displacement_point[1], point[2] + displacement_point[2]]

    return point

def gen_next_point_local(leg, dir, origin_point, id_of_point, list_of_pints):
    point = list_of_pints[id_of_point]
    point = [math.sin(math.radians(dir))*point[0], math.cos(math.radians(dir))*point[0], point[1]]
    if origin_point[0] > 0:
        displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1])+math.atan(origin_point[1]/origin_point[0]))*math.sqrt(origin_point[0]**2+origin_point[1]**2) + config.data["legMountX"][leg-1],
                              math.sin(math.radians(config.data["legMountAngle"][leg-1])+math.atan(origin_point[1]/origin_point[0]))*math.sqrt(origin_point[0]**2+origin_point[1]**2) + config.data["legMountY"][leg-1],
                              origin_point[2]]
    elif origin_point[0] < 0:
        displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1])+math.atan(origin_point[1]/origin_point[0])+0.5*math.pi)*math.sqrt(origin_point[0]**2+origin_point[1]**2) + config.data["legMountX"][leg-1],
                              math.sin(math.radians(config.data["legMountAngle"][leg-1])+math.atan(origin_point[1]/origin_point[0])+0.5*math.pi)*math.sqrt(origin_point[0]**2+origin_point[1]**2) + config.data["legMountY"][leg-1],
                              origin_point[2]]
    else:
        displacement_point = [math.cos(math.radians(config.data["legMountAngle"][leg-1]))*origin_point[1] + config.data["legMountX"][leg-1],
                              math.sin(math.radians(config.data["legMountAngle"][leg-1]))*origin_point[1] + config.data["legMountY"][leg-1],
                              origin_point[2]]
    point = [point[0] + displacement_point[0], point[1] + displacement_point[1], point[2] + displacement_point[2]]

    return point

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


#points = gen_foot_path()
#new_points = []
#for i in range(0, len(points)):
#    new_points.append(gen_next_point(1, 0, [160, 0, -160], i, points))
#
#print(new_points)
#plot_3d_points(new_points)

