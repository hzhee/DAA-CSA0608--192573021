import heapq
n,k=map(int,input().split()); graph=[[] for _ in range(n)]
for _ in range(int(input())):
 a,b,w=map(int,input().split());graph[a-1].append((b-1,w))
d=[float('inf')]*n;d[k-1]=0;q=[(0,k-1)]
while q:
 x,u=heapq.heappop(q)
 if x!=d[u]:continue
 for v,w in graph[u]:
  if x+w<d[v]:d[v]=x+w;heapq.heappush(q,(d[v],v))
print(-1 if max(d)==float('inf') else max(d))
