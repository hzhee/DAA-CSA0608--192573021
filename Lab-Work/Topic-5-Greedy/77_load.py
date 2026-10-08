weights=sorted(map(int,input().split()),reverse=True);cap=int(input());total=0
for w in weights:
 if total+w<=cap:total+=w
print(total)
