from itertools import permutations

size = int(input("Enter matrix size: "))
cost = [list(map(int, input("Enter row costs: ").split())) for _ in range(size)]
best_cost = float("inf")
best_assignment = None

for assignment in permutations(range(size)):
    total = sum(cost[worker][assignment[worker]] for worker in range(size))
    if total < best_cost:
        best_cost = total
        best_assignment = assignment

print("Optimal assignment:", [(worker + 1, task + 1) for worker, task in enumerate(best_assignment)])
print("Total cost:", best_cost)
