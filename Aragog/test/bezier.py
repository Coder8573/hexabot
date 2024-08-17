import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math


def bernstein_poly(i, n, t):
    """Bernstein-Polynom b_{i,n} bei t."""
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))


def comb(n, k):
    """Kombinationsfunktion nCk."""
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def bezier_curve(points, num_points=100):
    """Erstellt eine Bezierkurve aus gegebenen 3D-Punkten."""
    n = len(points) - 1
    t = np.linspace(0, 1, num_points)
    curve = np.zeros((num_points, 3))

    for i in range(n + 1):
        bernstein = bernstein_poly(i, n, t)
        curve += np.outer(bernstein, points[i])

    return curve


def bezier_length(curve):
    """Berechnet die Länge einer 3D-Bezierkurve."""
    diff = np.diff(curve, axis=0)
    length = np.sum(np.sqrt(np.sum(diff ** 2, axis=1)))
    return length


def generate_points(curve, distance):
    """Generiert Punkte entlang der Bezierkurve in festen Abständen."""
    total_length = bezier_length(curve)
    num_points = int(total_length // distance)
    t_values = np.linspace(0, 1, len(curve))
    lengths = np.cumsum(np.sqrt(np.sum(np.diff(curve, axis=0) ** 2, axis=1)))
    lengths = np.insert(lengths, 0, 0)

    points = [curve[0]]
    current_length = 0

    for i in range(1, len(curve)):
        segment_length = np.sqrt(np.sum((curve[i] - curve[i - 1]) ** 2))
        while current_length + segment_length >= len(points) * distance:
            points.append(
                curve[i - 1] + (curve[i] - curve[i - 1]) * ((len(points) * distance - current_length) / segment_length))
        current_length += segment_length

    if len(points) < num_points + 1:
        points.append(curve[-1])

    return np.array(points)


def set_axes_equal(ax):
    """Stellt sicher, dass die 3D-Achsen die gleiche Skalierung haben."""
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])

    max_range = max(x_range, y_range, z_range)

    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)

    ax.set_xlim3d([x_middle - max_range / 2, x_middle + max_range / 2])
    ax.set_ylim3d([y_middle - max_range / 2, y_middle + max_range / 2])
    ax.set_zlim3d([z_middle - max_range / 2, z_middle + max_range / 2])


def plot_bezier_curve(points, curve, generated_points=None):
    """Plottet die Bezierkurve, die Kontrollpunkte und die generierten Punkte."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Kontrollpunkte plotten
    points = np.array(points)
    ax.plot(points[:, 0], points[:, 1], points[:, 2], 'ro--', label='Kontrollpunkte')

    # Bezierkurve plotten
    ax.plot(curve[:, 0], curve[:, 1], curve[:, 2], 'b-', label='Bezierkurve')

    # Generierte Punkte plotten
    if generated_points is not None:
        generated_points = np.array(generated_points)
        ax.plot(generated_points[:, 0], generated_points[:, 1], generated_points[:, 2], 'go', label='Generierte Punkte')

    # Achsen gleich skalieren
    set_axes_equal(ax)

    ax.legend()
    plt.show()

def print_points(points):
    temp = points.tolist()
    for i in temp:
        print(i)


# Beispiel-Punkte
points = [
    [8, 4, 0],
    [8, 3.5, 4],
    [8, -3.5, 4],
    [8, -4, 0]
]



# Bezierkurve berechnen
curve = bezier_curve(points)

# Punkte in festen Abständen generieren
distance = 0.5
generated_points = generate_points(curve, distance)

# Kurve plotten
plot_bezier_curve(points, curve, generated_points)

print_points(generated_points)