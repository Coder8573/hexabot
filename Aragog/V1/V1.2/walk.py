import math
from scipy.integrate import quad
from scipy.optimize import newton
import matplotlib.pyplot as plt

import config
import kinematics

calc = kinematics.Calc()

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
    length, _ = quad(integrand, a=0, b=1)
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

def difference_between_two_points(point1, point2):
    if len(point1) == 2:
        return math.sqrt((point2[0]-point1[0])**2 +
                         (point2[1]-point1[1])**2)

    if len(point1) == 3:
        return math.sqrt((point2[0] - point1[0]) ** 2 +
                         (point2[1] - point1[1]) ** 2 +
                         (point2[2] - point1[2]) ** 2)

def gen_point(t, curve_len, curve_boundary):
    t_i = inverse_L(t, curve_boundary, curve_len)
    point = bezier_curve(t_i, curve_boundary)
    return point

def gen_top_path(leg, dir, progress, origin_point):
    progress = progress/100
    if 0 <= progress < curve_left_len/top_length:
        point = gen_point(progress*top_length, curve_left_len, curve_left_boundary)

    elif curve_left_len/top_length <= progress < (curve_left_len+curve_top_len)/top_length:
        point = gen_point(progress*top_length, curve_top_len, curve_top_boundary)

    elif (curve_left_len+curve_top_len)/top_length <= progress <= 1:
        point = gen_point(progress*top_length, curve_right_len, curve_right_boundary)

    point = [0, 0, 0]
    point = [math.sin(math.radians(dir+config.data["legMountAngle"][leg-1])) * point[0] + origin_point[0], math.cos(math.radians(dir+config.data["legMountAngle"][leg-1])) * point[0] + origin_point[1], point[1] + origin_point[2]]
    return point


def gen_next_point(leg, dir, origin_point, last_points, stepsize, walk_progress, inverted):
    if inverted:
        point = [last_points[0] + math.sin(math.radians(dir)) * stepsize,
                 last_points[1] + math.cos(math.radians(dir)) * stepsize,
                 last_points[2]]
    else:
        point = [last_points[0]-math.sin(math.radians(dir))*stepsize,
                 last_points[1]-math.cos(math.radians(dir))*stepsize,
                 last_points[2]]
    distance_between_points = difference_between_two_points(origin_point[0:-1], point[0:-1])
    walk_progress = (distance_between_points/config.data["step_length"])*50
    print(f"walk progress: {walk_progress}")
    print(f"distance between points: {distance_between_points}")

    if distance_between_points > step_length/2:
        inverted = not inverted
    return point, walk_progress, inverted


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


curve_top_len = curve_length(curve_top_boundary)
curve_left_len = curve_length(curve_left_boundary)
curve_right_len = curve_length(curve_right_boundary)

top_length = curve_top_len + curve_left_len + curve_right_len