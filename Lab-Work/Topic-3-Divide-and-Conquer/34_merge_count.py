count = 0
def sort(a):
    global count
    if len(a) < 2: return a
    l, r = sort(a[:len(a)//2]), sort(a[len(a)//2:]); out=[]
    while l and r:
        count += 1; out.append(l.pop(0) if l[0] < r[0] else r.pop(0))
    return out+l+r
print(sort(list(map(int,input().split())))); print("Comparisons:",count)
