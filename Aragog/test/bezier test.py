from scipy.integrate import quad
from scipy.optimize import newton
import matplotlib.pyplot as plt



# Bezier Kurve erstellen
def bezier_curve(t, P0, P1, P2):
    x = (1-t)**2 * P0[0] + 2*(1-t) * t * P1[0] + t**2 * P2[0]
    y = (1-t)**2 * P0[1] + 2*(1-t) * t * P1[1] + t**2 * P2[1]
    return [x, y]


# Ableiten (derivation = Ableiten)
def bezier_curve_derivation(t, P0, P1, P2):
    x = 2*(1-t) * (P1[0] - P0[0]) + 2*t * (P2[0] - P1[0])
    y = 2*(1-t) * (P1[1] - P0[1]) + 2*t * (P2[1] - P1[1])
    return [x, y]

# Satz des Pytagoras
def pyt(v):
    # squrt(x**2 + y**2)
    return (v[0]**2 + v[1]**2)**0.5

# Gesamtlänge der Kurve berechnen
def curve_length(P0, P1, P2):
    integrand = lambda t: pyt(bezier_curve_derivation(t, P0, P1, P2))
    length, _ = quad(integrand, 0, 1)
    return length


# Längen-Funktion L(t)
def L_t(t, P0, P1, P2):
    integrand = lambda u: pyt(bezier_curve_derivation(u, P0, P1, P2))
    length, _ = quad(integrand, 0, t)
    return length

# Umkehrfunktion L^-1(s) finden
def inverse_L(s, P0, P1, P2, L):
    func = lambda t: L_t(t, P0, P1, P2) - s
    t_initial_guess = s / L
    t_solution = newton(func, t_initial_guess)
    return t_solution

step_length = 240
step_curviture_distance = 80
step_height = 100


# Beispiel für eine quadratische Bézier-Kurve
P0 = [-120, 40]
P1 = [0, 100]
P2 = [120, 40]

L = curve_length(P0, P1, P2)
print(L)

# Gleichmäßig verteilte Punkte berechnen
n = 121  # Anzahl der gewünschten Punkte
points = []
for i in range(n):
    s_i = i * L / (n - 1)
    t_i = inverse_L(s_i, P0, P1, P2, L)
    points.append(bezier_curve(t_i, P0, P1, P2))

# Bézier-Kurve und Punkte plotten
t_values = [i / 99.0 for i in range(100)]
curve = [bezier_curve(t, P0, P1, P2) for t in t_values]

curve_x = [p[0] for p in curve]
curve_y = [p[1] for p in curve]
points_x = [p[0] for p in points]
points_y = [p[1] for p in points]

plt.figure(figsize=(8, 6))
plt.plot(curve_x, curve_y, label="Bézier-Kurve", color="blue")
plt.scatter(points_x, points_y, color="red", label="Gleichmäßig verteilte Punkte")
plt.scatter([P0[0], P1[0], P2[0]], [P0[1], P1[1], P2[1]], color="green", label="Kontrollpunkte")
plt.legend()
plt.title("Quadratische Bézier-Kurve mit gleichmäßig verteilten Punkten")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.axis("equal")
plt.show()
