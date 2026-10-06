arr = list(map(int, input("Enter sorted elements: ").split()))
k = int(input("Enter k: "))
number = 1

for value in arr:
    while number < value and k > 0:
        k -= 1
        if k == 0:
            print(number)
            raise SystemExit
        number += 1
    number = value + 1

print(number + k - 1)
