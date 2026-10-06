from math import atan2

count = int(input("Enter number of points: "))
points = [tuple(map(float, input("Enter x y: ").split())) for _ in range(count)]
hull = []

for first in range(count):
    for second in range(first + 1, count):
        sides = []
        for third in range(count):
            cross = ((points[second][0] - points[first][0]) * (points[third][1] - points[first][1]) -
                     (points[second][1] - points[first][1]) * (points[third][0] - points[first][0]))
            if cross != 0:
                sides.append(cross > 0)
        if not sides or all(sides) or not any(sides):
            for point in (points[first], points[second]):
                if point not in hull:
                    hull.append(point)

center_x = sum(point[0] for point in hull) / len(hull)
center_y = sum(point[1] for point in hull) / len(hull)
hull.sort(key=lambda point: atan2(point[1] - center_y, point[0] - center_x))
print(hull)
