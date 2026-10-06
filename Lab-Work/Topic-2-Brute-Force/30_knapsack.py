count = int(input("Enter number of items: "))
weights = list(map(int, input("Enter weights: ").split()))
values = list(map(int, input("Enter values: ").split()))
capacity = int(input("Enter capacity: "))
best_value = 0
best_items = []

for mask in range(1 << count):
    chosen = [index for index in range(count) if mask & (1 << index)]
    weight = sum(weights[index] for index in chosen)
    value = sum(values[index] for index in chosen)
    if weight <= capacity and value > best_value:
        best_value = value
        best_items = chosen

print("Optimal selection:", best_items)
print("Total value:", best_value)
