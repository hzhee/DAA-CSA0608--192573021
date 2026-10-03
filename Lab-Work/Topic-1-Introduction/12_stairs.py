n = int(input("Enter number of steps: "))

if n <= 1:
    ways = 1
else:
    previous_two = 1
    previous_one = 1

    for _ in range(2, n + 1):
        ways = previous_one + previous_two
        previous_two = previous_one
        previous_one = ways

    ways = previous_one

print("Number of ways:", ways)
