n=int(input()); d=[list(map(float,input().split())) for _ in range(n)]; limit=float(input())
for k in range(n):
 for i in range(n):
  for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
print(min(range(n),key=lambda i:(sum(x<=limit for x in d[i])-1,-i)))
