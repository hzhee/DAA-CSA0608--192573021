from itertools import permutations
print([list(x) for x in sorted(set(permutations(map(int,input().split()))))])
