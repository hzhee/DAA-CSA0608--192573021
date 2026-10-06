def find(a, k):
    if len(a) <= 5: return sorted(a)[k]
    pivot = find([sorted(a[i:i+5])[len(a[i:i+5])//2] for i in range(0,len(a),5)], len(a)//10)
    low=[x for x in a if x<pivot]; high=[x for x in a if x>pivot]
    return find(low,k) if k<len(low) else pivot if k<len(a)-len(high) else find(high,k-len(a)+len(high))
a=list(map(int,input().split())); print(find(a,int(input())-1))
