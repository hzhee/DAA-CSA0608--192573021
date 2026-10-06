from itertools import permutations
from math import sqrt

count = int(input("Enter number of cities: "))
cities = [tuple(map(float, input("Enter x y: ").split())) for _ in range(count)]
best_path = None
best_distance = float("inf")

for order in permutations(range(1, count)):
    path = (0,) + order + (0,)
    distance = sum(sqrt((cities[path[i]][0] - cities[path[i + 1]][0]) ** 2 + (cities[path[i]][1] - cities[path[i + 1]][1]) ** 2) for i in range(count))
    if distance < best_distance:
        best_distance = distance
        best_path = path

print("Shortest distance:", best_distance)
print("Shortest path:", [cities[index] for index in best_path])
