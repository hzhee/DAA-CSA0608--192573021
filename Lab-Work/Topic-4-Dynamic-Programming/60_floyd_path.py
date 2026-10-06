n=int(input()); d=[list(map(float,input().split())) for _ in range(n)]
for k in range(n):
 for i in range(n):
  for j in range(n): d[i][j]=min(d[i][j],d[i][k]+d[k][j])
a,b=map(int,input().split()); print(d[a][b])
