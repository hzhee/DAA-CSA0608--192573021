values = list(map(int, input("Enter elements: ").split()))
left = 0
right = len(values) - 1

while left < right:
    middle = (left + right) // 2
    if values[middle] < values[middle + 1]:
        left = middle + 1
    else:
        right = middle

print(left)
