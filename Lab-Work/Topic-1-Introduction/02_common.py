nums1 = list(map(int, input("Enter elements of nums1: ").split()))
nums2 = list(map(int, input("Enter elements of nums2: ").split()))

set1 = set(nums1)
set2 = set(nums2)

answer1 = 0
answer2 = 0

for num in nums1:
    if num in set2:
        answer1 += 1

for num in nums2:
    if num in set1:
        answer2 += 1

print("Output:", [answer1, answer2])