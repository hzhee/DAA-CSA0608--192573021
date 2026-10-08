from itertools import product
clauses=[list(map(int,part.split(','))) for part in input().split()]; variables=max(abs(x) for clause in clauses for x in clause)
for values in product([False,True],repeat=variables):
    if all(any(values[abs(x)-1] if x>0 else not values[abs(x)-1] for x in clause) for clause in clauses):print(values);break
else:print(False)
