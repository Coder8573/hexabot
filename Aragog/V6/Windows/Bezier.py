

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



