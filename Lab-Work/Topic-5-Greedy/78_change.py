coins=sorted(map(int,input().split()),reverse=True);amount=int(input());count=0
for coin in coins: count,amount=count+amount//coin,amount%coin
print(count if not amount else -1)
