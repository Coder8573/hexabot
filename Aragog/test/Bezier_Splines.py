import matplotlib.pyplot as plt
import numpy as np


def bezier_point(p0, p1, p2, p3, t):
    """
    Berechnet einen Punkt auf einer kubischen Bézier-Kurve für einen gegebenen Parameter t.

    Args:
        p0, p1, p2, p3 (tuple): Kontrollpunkte der Bézier-Kurve.
        t (float): Parameter (0 <= t <= 1).

    Returns:
        tuple: Punkt auf der Bézier-Kurve.
    """
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return (x, y)


def bezier_curve(points, step_size=0.01):
    """
    Berechnet eine Reihe von Punkten auf einer Bézier-Kurve, die durch eine Liste von Punkten definiert ist.

    Args:
        points (list of tuples): Liste der Punkte, durch die die Kurve verlaufen soll.
        step_size (float): Schrittgröße für die Parameter t (je kleiner, desto genauer).

    Returns:
        list of tuples: Punkte auf der Bézier-Kurve.
    """
    curve_points = []
    for i in range(0, len(points) - 3, 3):
        p0, p1, p2, p3 = points[i], points[i + 1], points[i + 2], points[i + 3]
        t = 0
        while t <= 1:
            curve_points.append(bezier_point(p0, p1, p2, p3, t))
            t += step_size
    return curve_points


def distance(p1, p2):
    """Berechnet die euklidische Distanz zwischen zwei Punkten."""
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def generate_evenly_spaced_points(curve_points, fixed_distance):
    """
    Generiert Punkte gleichmäßig entlang der Kurve in festen Abständen.

    Args:
        curve_points (list of tuples): Punkte auf der Bézier-Kurve.
        fixed_distance (float): Fester Abstand zwischen den Punkten.

    Returns:
        list of tuples: Gleichmäßig verteilte Punkte entlang der Kurve.
    """
    evenly_spaced_points = [curve_points[0]]
    accumulated_distance = 0

    for i in range(1, len(curve_points)):
        accumulated_distance += distance(curve_points[i - 1], curve_points[i])
        while accumulated_distance >= fixed_distance:
            extra_distance = accumulated_distance - fixed_distance
            direction_vector = (
                (curve_points[i][0] - curve_points[i - 1][0]) / distance(curve_points[i], curve_points[i - 1]),
                (curve_points[i][1] - curve_points[i - 1][1]) / distance(curve_points[i], curve_points[i - 1])
            )
            new_point = (
                curve_points[i - 1][0] + direction_vector[0] * (fixed_distance - extra_distance),
                curve_points[i - 1][1] + direction_vector[1] * (fixed_distance - extra_distance)
            )
            evenly_spaced_points.append(new_point)
            accumulated_distance = extra_distance

    return evenly_spaced_points


def plot_points_and_curve(points, curve, evenly_spaced_points):
    """
    Plottet die Punkte, die Bézier-Kurve und die gleichmäßig verteilten Punkte.

    Args:
        points (list of tuples): Liste der Punkte, durch die die Kurve verlaufen soll.
        curve (list of tuples): Punkte auf der Bézier-Kurve.
        evenly_spaced_points (list of tuples): Gleichmäßig verteilte Punkte entlang der Kurve.
    """
    points_x, points_y = zip(*points)
    curve_x, curve_y = zip(*curve)
    evenly_spaced_x, evenly_spaced_y = zip(*evenly_spaced_points)

    plt.figure(figsize=(10, 6))
    plt.plot(points_x, points_y, 'ro-', label='Kontrollpunkte')
    plt.plot(curve_x, curve_y, 'b-', label='Bézier-Kurve')
    plt.plot(evenly_spaced_x, evenly_spaced_y, 'go-', label='Gleichmäßig verteilte Punkte')
    plt.axis('equal')  # Achsenskalierung gleichsetzen
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Liste der Punkte (sollte Anzahl der Punkte = 3n + 1 sein, z.B. 4, 7, 10, etc.)
    points = [(-120, -160), (-160, -160), (-160, -110), (0, -110), (160, -110), (160, -160), (120, -160), (80, -160), (-80, -160), (-120, -160)]

    # Berechne die Bézier-Kurve
    curve = bezier_curve(points)

    # Generiere gleichmäßig verteilte Punkte entlang der Kurve
    fixed_distance = 10
    evenly_spaced_points = generate_evenly_spaced_points(curve, fixed_distance)

    # Plotte die Punkte, die Kurve und die gleichmäßig verteilten Punkte
    plot_points_and_curve(points, curve, evenly_spaced_points)
