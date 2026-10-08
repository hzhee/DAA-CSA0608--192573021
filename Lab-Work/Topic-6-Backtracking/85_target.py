a=list(map(int,input().split()));target=int(input());ans=0
def go(i,total):
 global ans
 if i==len(a):ans+=total==target;return
 go(i+1,total+a[i]);go(i+1,total-a[i])
go(0,0);print(ans)
