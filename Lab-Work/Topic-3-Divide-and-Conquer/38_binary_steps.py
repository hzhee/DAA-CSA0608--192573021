a=list(map(int,input().split())); key=int(input()); lo=0; hi=len(a)-1
while lo<=hi:
    mid=(lo+hi)//2; print("Mid:",mid+1)
    if a[mid]==key: print("Position:",mid+1); break
    if a[mid]<key: lo=mid+1
    else: hi=mid-1
