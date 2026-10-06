import heapq
n=int(input()); start,end=map(int,input().split()); graph=[[] for _ in range(n)]
for _ in range(int(input())):
 a,b,p=input().split(); a=int(a);b=int(b);p=float(p); graph[a].append((b,p));graph[b].append((a,p))
best=[0]*n;best[start]=1;q=[(-1,start)]
while q:
 p,u=heapq.heappop(q);p=-p
 for v,w in graph[u]:
  if p*w>best[v]:best[v]=p*w;heapq.heappush(q,(-best[v],v))
print(best[end])
