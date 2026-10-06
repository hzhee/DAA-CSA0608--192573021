from math import atan2

count = int(input("Enter number of points: "))
points = [tuple(map(float, input("Enter x y: ").split())) for _ in range(count)]
hull = []

for first in range(count):
    for second in range(count):
        if first == second:
            continue
        side = 0
        valid = True
        for third in range(count):
            value = ((points[second][0] - points[first][0]) * (points[third][1] - points[first][1]) -
                     (points[second][1] - points[first][1]) * (points[third][0] - points[first][0]))
            if value != 0:
                if side == 0:
                    side = 1 if value > 0 else -1
                elif (value > 0) != (side > 0):
                    valid = False
                    break
        if valid:
            if points[first] not in hull:
                hull.append(points[first])
            if points[second] not in hull:
                hull.append(points[second])

center_x = sum(point[0] for point in hull) / len(hull)
center_y = sum(point[1] for point in hull) / len(hull)
hull.sort(key=lambda point: atan2(point[1] - center_y, point[0] - center_x))
print(hull)
