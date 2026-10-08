jobs=sorted(map(int,input().split()),reverse=True); workers=int(input()); loads=[0]*workers
for job in jobs: i=loads.index(min(loads));loads[i]+=job
print(max(loads))
