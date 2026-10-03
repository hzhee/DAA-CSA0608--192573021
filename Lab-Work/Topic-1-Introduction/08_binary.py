nums = list(map(int, input("Enter sorted elements: ").split()))
key = int(input("Enter the element to search: "))

low = 0
high = len(nums) - 1
found = -1

while low <= high:
    mid = (low + high) // 2

    if nums[mid] == key:
        found = mid
        break
    elif nums[mid] < key:
        low = mid + 1
    else:
        high = mid - 1

if found != -1:
    print("Element", key, "is found at index", found)
else:
    print("Element", key, "is not found")