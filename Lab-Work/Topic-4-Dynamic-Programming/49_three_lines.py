lines=[list(map(int,input().split())) for _ in range(3)]; print(sum(min(station) for station in zip(*lines)))
