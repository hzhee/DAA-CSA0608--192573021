def quick(a):
    if len(a)<2:return a
    p=a[0]; return quick([x for x in a[1:] if x<=p])+[p]+quick([x for x in a[1:] if x>p])
print(quick(list(map(int,input().split()))))
