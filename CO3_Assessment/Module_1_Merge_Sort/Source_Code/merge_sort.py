"""Stable merge sort trace for KartIQ nightly order consolidation."""

def merge(left, right, trace, depth):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # <= is the stability decision: equal timestamps stay left-first.
        if left[i][0] <= right[j][0]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    trace.append(f"{'  ' * depth}merge {left} + {right} -> {result}")
    return result

def merge_sort(items, trace, depth=0):
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left = merge_sort(items[:mid], trace, depth + 1)
    right = merge_sort(items[mid:], trace, depth + 1)
    return merge(left, right, trace, depth)

if __name__ == "__main__":
    orders = [(105, "O1"), (102, "O2"), (105, "O3"),
              (101, "O4"), (102, "O5"), (103, "O6")]
    trace = []
    ordered = merge_sort(orders, trace)
    print("Input:", orders)
    print("\nMerge trace:")
    print("\n".join(trace))
    print("\nSorted:", ordered)
    print("Stable check: timestamp 102 is O2 then O5; timestamp 105 is O1 then O3.")
