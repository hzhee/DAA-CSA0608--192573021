rows = int(input("Enter number of rows: "))
columns = int(input("Enter number of columns: "))
board = []

for _ in range(rows):
    board.append(list(map(int, input("Enter row values: ").split())))

next_board = [[0] * columns for _ in range(rows)]

for row in range(rows):
    for column in range(columns):
        live_neighbors = 0

        for row_move in (-1, 0, 1):
            for column_move in (-1, 0, 1):
                new_row = row + row_move
                new_column = column + column_move

                if (row_move != 0 or column_move != 0) and 0 <= new_row < rows and 0 <= new_column < columns:
                    live_neighbors += board[new_row][new_column]

        if board[row][column] == 1 and live_neighbors in (2, 3):
            next_board[row][column] = 1
        elif board[row][column] == 0 and live_neighbors == 3:
            next_board[row][column] = 1

print(next_board)
