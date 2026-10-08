vertices=input().split(); edges={tuple(edge.split(',')) for edge in input().split()}; path=[]
def solve(vertex):
    if len(path)==len(vertices):return True
    for next_vertex in vertices:
        if next_vertex not in path and (not path or (vertex,next_vertex)in edges or (next_vertex,vertex)in edges):
            path.append(next_vertex)
            if solve(next_vertex):return True
            path.pop()
    return False
print(solve(''),path)
