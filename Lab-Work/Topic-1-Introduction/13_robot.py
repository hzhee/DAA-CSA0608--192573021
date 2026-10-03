m = int(input("Enter number of rows: "))
n = int(input("Enter number of columns: "))

paths = [[1] * n for _ in range(m)]

for row in range(1, m):
    for column in range(1, n):
        paths[row][column] = paths[row - 1][column] + paths[row][column - 1]

print("Number of unique paths:", paths[m - 1][n - 1])
