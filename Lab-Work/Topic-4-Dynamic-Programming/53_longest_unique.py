s=input(); start=0; seen={}; best=0
for i,c in enumerate(s):
 if c in seen and seen[c]>=start: start=seen[c]+1
 seen[c]=i; best=max(best,i-start+1)
print(best)
