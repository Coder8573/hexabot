import numpy as np

import math
import matplotlib.pyplot as plt
import time

def bezier_length(p0, p1, p2, num_samples=1000):
    """
    Schätzt die Länge der quadratischen Bezier-Kurve durch Aufsummieren der Abstände zwischen diskreten Punkten.

    :param p0: Erster Kontrollpunkt (Liste oder Tupel mit 3 Werten)
    :param p1: Zweiter Kontrollpunkt (Liste oder Tupel mit 3 Werten)
    :param p2: Dritter Kontrollpunkt (Liste oder Tupel mit 3 Werten)
    :param num_samples: Anzahl der zu berechnenden Zwischenpunkte für die Längenabschätzung
    :return: Geschätzte Länge der Bezier-Kurve
    """
    t_values = np.linspace(0, 1, num_samples)
    curve_points = np.array(
        [(1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t ** 2 * np.array(p2) for t in t_values])
    lengths = np.linalg.norm(np.diff(curve_points, axis=0), axis=1)
    return np.sum(lengths)


def bezier_point_at_length(t, p0, p1, p2, num_samples=1000):
    """
    Berechnet einen Punkt auf der quadratischen Bezier-Kurve für einen Parameter t,
    wobei t mit der Länge der Kurve verknüpft ist.

    :param t: Parameter (0 <= t <= 1), der angibt, wie weit entlang der Kurve der Punkt liegt
    :param p0: Erster Kontrollpunkt (Liste oder Tupel mit 3 Werten)
    :param p1: Zweiter Kontrollpunkt (Liste oder Tupel mit 3 Werten)
    :param p2: Dritter Kontrollpunkt (Liste oder Tupel mit 3 Werten)
    :param num_samples: Anzahl der zu berechnenden Zwischenpunkte für die Längenabschätzung
    :return: Der Punkt auf der Bezier-Kurve bei t * Länge der Kurve
    """
    # Berechne die Länge der Kurve
    total_length = bezier_length(p0, p1, p2, num_samples)
    target_length = t * total_length

    # Diskretisiere die Kurve und berechne die kumulative Länge
    t_values = np.linspace(0, 1, num_samples)
    curve_points = np.array(
        [(1 - t_val) ** 2 * np.array(p0) + 2 * (1 - t_val) * t_val * np.array(p1) + t_val ** 2 * np.array(p2) for t_val
         in t_values])
    distances = np.cumsum(np.linalg.norm(np.diff(curve_points, axis=0), axis=1))

    # Finde den Punkt auf der Kurve, dessen kumulative Länge am nächsten zur gewünschten Länge ist
    closest_index = np.searchsorted(distances, target_length)

    # Interpoliere zwischen den Punkten, falls notwendig
    if closest_index == 0:
        return curve_points[0]
    elif closest_index >= len(curve_points):
        return curve_points[-1]
    else:
        # Lineare Interpolation zwischen den beiden nächsten Punkten
        prev_point = curve_points[closest_index - 1]
        next_point = curve_points[closest_index]
        prev_distance = distances[closest_index - 1]
        next_distance = distances[closest_index]
        interpolation_factor = (target_length - prev_distance) / (next_distance - prev_distance)
        return prev_point + interpolation_factor * (next_point - prev_point)



def distance_between_points(point_a, point_b):
    return math.sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2 + (point_a[2]-point_b[2])**2)



points = [[180, 80, 0], [180, 0, 80], [180, -80, 0]]
test_points = []
test_points.extend(points)

start = time.time()
for i in range(0, 1001):
    t = i/1000
    test_points.append(bezier_point_at_length(t, points[0], points[1], points[2]))
    #print(distance_between_points(test_points[i+2], test_points[i+3]))
end = time.time()
print(end - start)


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

plot_3d_points(test_points)


# execution time: 11.868sek / 100 points = 0,11868sek/point