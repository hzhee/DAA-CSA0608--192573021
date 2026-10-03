nums = list(map(int, input("Enter money in each house: ").split()))


def rob_line(houses):
    previous_two = 0
    previous_one = 0

    for money in houses:
        current = max(previous_one, previous_two + money)
        previous_two = previous_one
        previous_one = current

    return previous_one


if len(nums) == 1:
    maximum_money = nums[0]
else:
    maximum_money = max(rob_line(nums[:-1]), rob_line(nums[1:]))

print("Maximum money:", maximum_money)
