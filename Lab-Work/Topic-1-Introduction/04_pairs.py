nums = list(map(int, input("Enter the elements: ").split()))
k = int(input("Enter k: "))

count = 0
n = len(nums)

for i in range(n):
    for j in range(i + 1, n):
        if nums[i] == nums[j] and (i * j) % k == 0:
            count += 1

print("Number of valid pairs:", count)