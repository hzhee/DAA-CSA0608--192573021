from itertools import permutations
d=[list(map(int,input().split())) for _ in range(int(input()))]; n=len(d); best=min(((sum(d[p[i]][p[i+1]] for i in range(n)),p) for p in [(0,)+x+(0,) for x in permutations(range(1,n))])); print(best)
