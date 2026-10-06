a=list(map(int,input().split())); target=int(input()); best=[]; difference=float('inf')
for mask in range(1<<len(a)):
    subset=[a[i] for i in range(len(a)) if mask>>i&1]
    if abs(sum(subset)-target)<difference: best,difference=subset,abs(sum(subset)-target)
print(best, sum(best))
