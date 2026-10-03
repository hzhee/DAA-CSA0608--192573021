nums = list(map(int, input("Enter the elements: ").split()))

total = 0
n = len(nums)

for i in range(n):
    distinct = set()

    for j in range(i, n):
        distinct.add(nums[j])
        count = len(distinct)
        total += count * count

print("Sum of squares of distinct counts:", total)