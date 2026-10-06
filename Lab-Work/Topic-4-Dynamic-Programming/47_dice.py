sides,dice,target=map(int,input().split()); dp=[0]*(target+1); dp[0]=1
for _ in range(dice):
    next_dp=[0]*(target+1)
    for total in range(target+1):
        for face in range(1,sides+1):
            if total>=face: next_dp[total]+=dp[total-face]
    dp=next_dp
print(dp[target])
