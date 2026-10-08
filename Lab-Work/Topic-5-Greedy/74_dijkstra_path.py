import heapq
n,s,t=map(int,input().split());g=[[]for _ in range(n)]
for _ in range(int(input())):a,b,w=map(int,input().split());g[a].append((b,w))
d=[float('inf')]*n;d[s]=0;q=[(0,s)]
while q:
 x,u=heapq.heappop(q)
 if x!=d[u]:continue
 for v,w in g[u]:
  if x+w<d[v]:d[v]=x+w;heapq.heappush(q,(d[v],v))
print(d[t])
