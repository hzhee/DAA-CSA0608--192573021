def max_min(a):
    def solve(l,r):
        if l==r: return a[l],a[l],0
        m=(l+r)//2; lo1,hi1,c1=solve(l,m); lo2,hi2,c2=solve(m+1,r)
        return min(lo1,lo2),max(hi1,hi2),c1+c2+2
    return solve(0,len(a)-1)
def binary_search(a,x):
    l,r,c=0,len(a)-1,0
    while l<=r:
        c+=1; m=(l+r)//2
        if a[m]==x:return m,c
        if a[m]<x:l=m+1
        else:r=m-1
    return -1,c
if __name__=='__main__':
    a=[12,4,19,7,3,25,10,8]; print('MaxMin:',max_min(a)); print('Binary hit:',binary_search(sorted(a),19)); print('Binary miss:',binary_search(sorted(a),18))
