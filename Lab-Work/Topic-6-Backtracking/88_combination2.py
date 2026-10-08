a=sorted(map(int,input().split()));target=int(input());out=[]
def go(start,total,path):
 if total==target:out.append(path);return
 for i in range(start,len(a)):
  if i>start and a[i]==a[i-1]:continue
  if total+a[i]<=target:go(i+1,total+a[i],path+[a[i]])
go(0,0,[]);print(out)
