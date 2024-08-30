import numpy as np
import math
import matplotlib.pyplot as plt
from timeit import default_timer as timer

def quadratic_bezier_3d(p0, p1, p2, num_points=100):
    def bezier(t, p0, p1, p2):
        return (1 - t)**2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t**2 * np.array(p2)

    # Erstellt eine feine Unterteilung von t-Werten entlang der Bezier-Kurve
    t_values = np.linspace(0, 1, num_points * 10)
    curve_points = np.array([bezier(t, p0, p1, p2) for t in t_values])

    # Berechnet die kumulierte Länge der Kurve
    distances = np.cumsum(np.linalg.norm(np.diff(curve_points, axis=0), axis=1))
    total_length = distances[-1]

    # Interpoliert gleichmäßige Abstände entlang der Kurve
    uniform_distances = np.linspace(0, total_length, num_points)
    uniform_t_values = np.interp(uniform_distances, distances, t_values[1:])

    # Berechnet die gleichmäßig verteilten Punkte entlang der Kurve
    uniform_points = np.array([bezier(t, p0, p1, p2) for t in uniform_t_values])

    return uniform_points

def distance_between_points(point_a, point_b):
    return math.sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2 + (point_a[2]-point_b[2])**2)

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


points = [[180, 80, 0], [180, 0, 80], [180, -80, 0]]
test_points = []
test_points.extend(points)


start = timer()
test_points.extend(quadratic_bezier_3d(points[0], points[1], points[2], 1000000))
for i in range(0, 1000001):
    t = i/1000000
    #print(distance_between_points(test_points[i+1], test_points[i+2]))
end = timer()
print(end - start)


plot_3d_points(test_points)

# execution time: 71,01499550003791sek / 1000000 points = 0,0000710150sek/point = 14081points/sek