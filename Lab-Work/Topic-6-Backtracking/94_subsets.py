a=list(map(int,input().split()));print([[a[i]for i in range(len(a))if mask>>i&1]for mask in range(1<<len(a))])
