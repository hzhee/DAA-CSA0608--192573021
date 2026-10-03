m = int(input("Enter number of rows: "))
n = int(input("Enter number of columns: "))
steps = int(input("Enter number of steps: "))
start_row = int(input("Enter starting row: "))
start_column = int(input("Enter starting column: "))

paths = [[0] * n for _ in range(m)]

for _ in range(steps):
    next_paths = [[0] * n for _ in range(m)]

    for row in range(m):
        for column in range(n):
            for row_move, column_move in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                new_row = row + row_move
                new_column = column + column_move

                if new_row < 0 or new_row >= m or new_column < 0 or new_column >= n:
                    next_paths[row][column] += 1
                else:
                    next_paths[row][column] += paths[new_row][new_column]

    paths = next_paths

print("Number of paths:", paths[start_row][start_column])
