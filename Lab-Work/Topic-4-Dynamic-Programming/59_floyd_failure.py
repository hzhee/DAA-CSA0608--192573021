n=int(input()); d=[list(map(float,input().split())) for _ in range(n)]; a,b=map(int,input().split()); d[a][b]=d[b][a]=float('inf')
for k in range(n):
 for i in range(n):
  for j in range(n): d[i][j]=min(d[i][j],d[i][k]+d[k][j])
print(d)
