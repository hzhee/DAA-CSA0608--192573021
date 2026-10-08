vertices=set(map(int,input().split())); edges={tuple(map(int,x.split(','))) for x in input().split()}; cover=set()
while edges:
    a,b=next(iter(edges));cover|={a,b};edges={edge for edge in edges if a not in edge and b not in edge}
print(sorted(cover))
