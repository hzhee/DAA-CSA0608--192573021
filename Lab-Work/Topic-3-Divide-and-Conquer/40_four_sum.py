lists = [list(map(int, input().split())) for _ in range(4)]
count = 0
for a in lists[0]:
    for b in lists[1]:
        for c in lists[2]:
            for d in lists[3]:
                if a + b + c + d == 0:
                    count += 1
print(count)
