"""Quick sort using median-of-three pivot selection for KartIQ scores."""

def median_of_three_index(values, low, high):
    mid = (low + high) // 2
    trio = [(values[low], low), (values[mid], mid), (values[high], high)]
    return sorted(trio)[1][1]

def partition(values, low, high, trace):
    pivot_index = median_of_three_index(values, low, high)
    values[pivot_index], values[high] = values[high], values[pivot_index]
    pivot = values[high]
    i = low
    for j in range(low, high):
        if values[j] <= pivot:
            values[i], values[j] = values[j], values[i]
            i += 1
    values[i], values[high] = values[high], values[i]
    trace.append(f"partition [{low}:{high}] pivot={pivot}: {values}")
    return i

def quick_sort(values, low=0, high=None, trace=None):
    if high is None:
        high = len(values) - 1
    if trace is None:
        trace = []
    if low < high:
        pivot = partition(values, low, high, trace)
        quick_sort(values, low, pivot - 1, trace)
        quick_sort(values, pivot + 1, high, trace)
    return trace

if __name__ == "__main__":
    scores = [42, 17, 63, 8, 55, 29]
    print("Input:", scores)
    trace = quick_sort(scores)
    print("\nPartition trace:")
    print("\n".join(trace))
    print("\nSorted:", scores)
