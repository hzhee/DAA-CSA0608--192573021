a=sorted(map(int,input().split())); target=int(input()); reach=0; added=0
for coin in a:
 while coin>reach+1 and reach<target: reach+=reach+1;added+=1
 reach+=coin
print(added + (reach<target))
