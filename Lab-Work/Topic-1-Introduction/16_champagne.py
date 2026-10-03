poured = int(input("Enter poured cups: "))
query_row = int(input("Enter query row: "))
query_glass = int(input("Enter query glass: "))

tower = [[0.0] * (query_row + 2) for _ in range(query_row + 2)]
tower[0][0] = poured

for row in range(query_row):
    for glass in range(row + 1):
        if tower[row][glass] > 1:
            extra = (tower[row][glass] - 1) / 2
            tower[row + 1][glass] += extra
            tower[row + 1][glass + 1] += extra

fullness = min(1, tower[query_row][query_glass])
print(f"{fullness:.5f}")
