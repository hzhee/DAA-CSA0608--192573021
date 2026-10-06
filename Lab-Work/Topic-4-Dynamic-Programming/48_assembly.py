n=int(input()); a1=list(map(int,input().split())); a2=list(map(int,input().split())); t1=list(map(int,input().split())); t2=list(map(int,input().split())); e1,e2,x1,x2=map(int,input().split())
f1,f2=e1+a1[0],e2+a2[0]
for i in range(1,n): f1,f2=min(f1+a1[i],f2+t2[i-1]+a1[i]),min(f2+a2[i],f1+t1[i-1]+a2[i])
print(min(f1+x1,f2+x2))
