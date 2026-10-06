a=list(map(int,input().split())); target=int(input()); found=False
for mask in range(1<<len(a)):
    if sum(a[i] for i in range(len(a)) if mask>>i&1)==target: found=True; break
print(found)
