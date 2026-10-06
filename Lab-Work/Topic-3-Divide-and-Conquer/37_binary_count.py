a=list(map(int,input().split())); key=int(input()); lo=0; hi=len(a)-1; c=0
while lo<=hi:
    c+=1; mid=(lo+hi)//2
    if a[mid]==key: print(mid+1); break
    if a[mid]<key: lo=mid+1
    else: hi=mid-1
else: print(-1)
print("Comparisons:",c)
