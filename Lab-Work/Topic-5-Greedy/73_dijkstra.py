import heapq
n=int(input());g=[list(map(float,input().split())) for _ in range(n)];source=int(input());d=[float('inf')]*n;d[source]=0;q=[(0,source)]
while q:
 x,u=heapq.heappop(q)
 for v,w in enumerate(g[u]):
  if w<float('inf') and x+w<d[v]:d[v]=x+w;heapq.heappush(q,(d[v],v))
print(d)
