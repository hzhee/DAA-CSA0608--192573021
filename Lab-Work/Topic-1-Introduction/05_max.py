nums = list(map(int, input("Enter the elements: ").split()))

if len(nums) == 0:
    print("List is empty")
else:
    maximum = nums[0]

    for num in nums:
        if num > maximum:
            maximum = num

    print("Maximum element:", maximum)