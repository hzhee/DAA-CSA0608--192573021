values = list(map(int, input("Enter elements: ").split()))

for index in range(len(values)):
    smallest = index

    for next_index in range(index + 1, len(values)):
        if values[next_index] < values[smallest]:
            smallest = next_index

    values[index], values[smallest] = values[smallest], values[index]
    print("After pass", index + 1, ":", values)

print("Sorted array:", values)
