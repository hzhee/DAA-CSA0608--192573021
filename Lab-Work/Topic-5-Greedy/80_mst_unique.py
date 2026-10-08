n=int(input());edges=[tuple(map(int,input().split()))for _ in range(int(input()))];weights={w for _,_,w in edges};print('Unique' if len(weights)==len(edges) else 'Not unique')
