nums = list(map(int, input("Enter the elements: ").split()))

unique = []

for num in nums:
    if num not in unique:
        unique.append(num)

print("Unique elements:", unique)