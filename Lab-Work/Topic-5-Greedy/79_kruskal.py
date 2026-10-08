n=int(input());edges=[tuple(map(int,input().split()))for _ in range(int(input()))];parent=list(range(n))
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
ans=[]
for u,v,w in sorted(edges,key=lambda x:x[2]):
 a,b=find(u),find(v)
 if a!=b:parent[a]=b;ans.append((u,v,w))
print(ans,sum(x[2]for x in ans))
