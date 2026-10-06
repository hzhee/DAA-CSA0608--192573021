def quick(a):
    if len(a)<2:return a
    p=a[len(a)//2]; rest=a[:len(a)//2]+a[len(a)//2+1:]
    return quick([x for x in rest if x<=p])+[p]+quick([x for x in rest if x>p])
print(quick(list(map(int,input().split()))))
