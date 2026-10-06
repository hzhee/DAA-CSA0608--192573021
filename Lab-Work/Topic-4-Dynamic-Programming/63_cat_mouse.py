graph=[list(map(int,row.split())) for row in input().split(';')]; print('Mouse can reach hole' if 0 in graph[1] else 'Game state requires search')
