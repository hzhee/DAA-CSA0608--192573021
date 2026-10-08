start=list(map(int,input().split()));end=list(map(int,input().split()));profit=list(map(int,input().split())); jobs=sorted(zip(end,start,profit)); dp=[0]*(len(jobs)+1)
for i,(e,s,p) in enumerate(jobs,1): dp[i]=max(dp[i-1],p+max((dp[j] for j in range(i) if jobs[j][0]<=s),default=0))
print(dp[-1])
