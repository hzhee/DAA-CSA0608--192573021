def sort(a):
    if len(a) < 2: return a
    left, right = sort(a[:len(a)//2]), sort(a[len(a)//2:])
    result = []
    while left and right: result.append(left.pop(0) if left[0] < right[0] else right.pop(0))
    return result + left + right
print(sort(list(map(int, input().split()))))
