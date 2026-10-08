a=list(map(int,input().split()));print(sum(min(a[i:j]) for i in range(len(a)) for j in range(i+1,len(a)+1))%(10**9+7))
