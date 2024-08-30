import math

from scipy.integrate import quad
from scipy.optimize import newton

import matplotlib.pyplot as plt


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


points = gen_foot_path()
new_points = []
for i in range(0, len(points)):
    new_points.append(gen_next_point(1, 0, [160, 0, -160], i, points))

print(new_points)
plot_3d_points(new_points)

