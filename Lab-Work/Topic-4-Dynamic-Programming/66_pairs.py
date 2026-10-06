a=list(map(int,input().split())); print(sum(a[:i].count(x) for i,x in enumerate(a)))
