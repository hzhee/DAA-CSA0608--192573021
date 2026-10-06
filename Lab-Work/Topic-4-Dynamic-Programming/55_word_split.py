s=input(); words=set(input().split()); dp=[True]+[False]*len(s)
for i in range(1,len(s)+1): dp[i]=any(dp[j] and s[j:i] in words for j in range(i))
print('Yes' if dp[-1] else 'No')
