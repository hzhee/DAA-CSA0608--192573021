n=int(input()); edges=[tuple(map(int,x.split(','))) for x in input().split()]; colors=[-1]*n
def solve(vertex,k):
    if vertex==n:return True
    for color in range(k):
        if all(colors[b]!=color for a,b in edges if a==vertex) and all(colors[a]!=color for a,b in edges if b==vertex):
            colors[vertex]=color
            if solve(vertex+1,k):return True
            colors[vertex]=-1
    return False
for k in range(1,n+1):
    if solve(0,k):print(k,colors);break
