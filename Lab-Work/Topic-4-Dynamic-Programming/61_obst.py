keys=list(map(int,input().split())); freq=list(map(int,input().split())); n=len(keys); cost=[[0]*n for _ in range(n)]
for i in range(n): cost[i][i]=freq[i]
for length in range(2,n+1):
 for i in range(n-length+1):
  j=i+length-1; total=sum(freq[i:j+1]); cost[i][j]=min((cost[i][r-1] if r>i else 0)+(cost[r+1][j] if r<j else 0)+total for r in range(i,j+1))
print(cost[0][-1])
