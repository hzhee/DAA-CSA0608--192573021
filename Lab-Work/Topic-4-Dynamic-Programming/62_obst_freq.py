freq=list(map(int,input().split())); n=len(freq); dp=[[0]*n for _ in range(n)]
for i in range(n): dp[i][i]=freq[i]
for size in range(2,n+1):
 for i in range(n-size+1):
  j=i+size-1; dp[i][j]=min((dp[i][r-1] if r>i else 0)+(dp[r+1][j] if r<j else 0)+sum(freq[i:j+1]) for r in range(i,j+1))
print(dp[0][-1])
