s = input("Enter a lowercase string: ")
groups = []
start = 0

for index in range(1, len(s) + 1):
    if index == len(s) or s[index] != s[start]:
        if index - start >= 3:
            groups.append([start, index - 1])
        start = index

print(groups)
