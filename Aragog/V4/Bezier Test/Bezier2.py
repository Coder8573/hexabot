import math
from timeit import default_timer as timer
import matplotlib.pyplot as plt

def binomial_coefficient(n, k):
    result = 1

    # calculate binomial coefficient by this formula
    # (n!) / (k! * (n-k)!)

    for i in range(1, k+1):
        result = result * (n-(k-i))
        result = result / i

    return result


def get_point_on_curve_2(points, num_of_points, t):
    result = [0, 0]
    for i in range(num_of_points):
        b = binomial_coefficient(num_of_points-1, i) * ((1-t)**(num_of_points - 1 - i)) * (t**i)
        result[0] = result[0] + b*points[i][0]
        result[1] = result[1] + b*points[i][1]

    return result


def get_point_on_curve_3(points, num_of_points, t):
    result = [0, 0, 0]
    for i in range(num_of_points):
        b = binomial_coefficient(num_of_points-1, i) * ((1-t)**(num_of_points - 1 - i)) * (t**i)
        result[0] = result[0] + b*points[i][0]
        result[1] = result[1] + b*points[i][1]
        result[2] = result[2] + b*points[i][2]


    return result

def distance_between_points(point_a, point_b):
    return math.sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2 + (point_a[2]-point_b[2])**2)


points = [[180, 80, 0], [180, 0, 80], [180, -80, 0]]
test_points = []
test_points.extend(points)

start = timer()
for i in range(0, 1000001):
    t = i/1000000
    test_points.append(get_point_on_curve_3(points, 3, t))
    #print(distance_between_points(test_points[i+2], test_points[i+3]))
end = timer()
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


# execution time: 2,521523699979298sek / 1000000 points = 0,0000025215sek/point = 396585 points/sek