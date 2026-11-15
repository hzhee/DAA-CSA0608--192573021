"""First-occurrence binary search for an already consolidated order list."""

def first_timestamp(orders, target, trace=False):
    low, high, answer = 0, len(orders) - 1, -1
    steps = []
    while low <= high:
        mid = low + (high - low) // 2
        timestamp = orders[mid][0]
        steps.append(f"low={low}, high={high}, mid={mid}, timestamp={timestamp}")
        if timestamp >= target:
            if timestamp == target:
                answer = mid
            high = mid - 1
        else:
            low = mid + 1
    return (answer, steps) if trace else answer

if __name__ == "__main__":
    orders = [(101, "O4"), (102, "O2"), (102, "O5"), (103, "O6"),
              (105, "O1"), (105, "O3")]
    index, steps = first_timestamp(orders, 102, trace=True)
    print("Consolidated orders:", orders)
    print("Search target: 102\n")
    print("\n".join(steps))
    print(f"\nFirst match: index {index}, order {orders[index]}")
