a=list(map(int,input().split()));target=int(input());out=[]
def go(start,total,path):
 if total==target:out.append(path);return
 for i in range(start,len(a)):
  if total+a[i]<=target:go(i,total+a[i],path+[a[i]])
go(0,0,[]);print(out)
