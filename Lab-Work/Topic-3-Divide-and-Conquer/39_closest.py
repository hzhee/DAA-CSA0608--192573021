points = [tuple(map(int, part.split(','))) for part in input("Enter x,y points: ").split()]
k = int(input("Enter k: "))
points.sort(key=lambda point: point[0] * point[0] + point[1] * point[1])
print(points[:k])
