haystack = input("Enter haystack: ")
needle = input("Enter needle: ")
position = -1

for start in range(len(haystack) - len(needle) + 1):
    if haystack[start:start + len(needle)] == needle:
        position = start
        break

print(position)
