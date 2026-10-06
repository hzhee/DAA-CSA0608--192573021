values = list(map(int, input("Enter elements: ").split()))

for last in range(len(values) - 1, 0, -1):
    swapped = False
    for index in range(last):
        if values[index] > values[index + 1]:
            values[index], values[index + 1] = values[index + 1], values[index]
            swapped = True
    if not swapped:
        break

print(values)
