n=int(input()); edges={tuple(map(int,x.split(','))) for x in input().split()}; path=[0]
def solve(vertex):
    if len(path)==n:return (vertex,0)in edges or (0,vertex)in edges
    for next_vertex in range(n):
        if next_vertex not in path and ((vertex,next_vertex)in edges or (next_vertex,vertex)in edges):
            path.append(next_vertex)
            if solve(next_vertex):return True
            path.pop()
    return False
print(path+[0] if solve(0) else [])
