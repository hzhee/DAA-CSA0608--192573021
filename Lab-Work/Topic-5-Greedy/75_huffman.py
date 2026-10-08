import heapq
chars=input().split();freq=list(map(int,input().split()));q=[[f,[c,'']]for c,f in zip(chars,freq)];heapq.heapify(q)
while len(q)>1:
 a=heapq.heappop(q);b=heapq.heappop(q)
 for x in a[1:]:x[1]='0'+x[1]
 for x in b[1:]:x[1]='1'+x[1]
 heapq.heappush(q,[a[0]+b[0]]+a[1:]+b[1:])
print(q[0][1:])
