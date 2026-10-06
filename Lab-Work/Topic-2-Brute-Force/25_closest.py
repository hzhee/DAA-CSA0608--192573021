from math import sqrt

count = int(input("Enter number of points: "))
points = [tuple(map(float, input("Enter x y: ").split())) for _ in range(count)]
best_pair = None
best_distance = float("inf")

for first in range(count):
    for second in range(first + 1, count):
        distance = sqrt((points[first][0] - points[second][0]) ** 2 + (points[first][1] - points[second][1]) ** 2)
        if distance < best_distance:
            best_distance = distance
            best_pair = (points[first], points[second])

print("Closest pair:", best_pair)
print("Minimum distance:", best_distance)
