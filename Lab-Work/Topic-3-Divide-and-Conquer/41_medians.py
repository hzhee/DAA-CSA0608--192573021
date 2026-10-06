def select(values, k):
    if len(values) <= 5:
        return sorted(values)[k]
    medians = [sorted(values[index:index + 5])[len(values[index:index + 5]) // 2] for index in range(0, len(values), 5)]
    pivot = select(medians, len(medians) // 2)
    small = [value for value in values if value < pivot]
    equal = [value for value in values if value == pivot]
    if k < len(small): return select(small, k)
    if k < len(small) + len(equal): return pivot
    return select([value for value in values if value > pivot], k - len(small) - len(equal))
a = list(map(int, input().split())); print(select(a, int(input()) - 1))
