universe=set(map(int,input().split())); sets=[set(map(int,part.split(','))) for part in input().split()]; chosen=[]
while universe:
    best=max(sets,key=lambda group:len(group&universe));chosen.append(sorted(best));universe-=best
print(chosen)
