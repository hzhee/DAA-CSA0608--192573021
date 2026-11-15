"""Original selected Day-4 challenge: maximum contiguous sales-period gain."""
def max_gain(a):
 def solve(l,r):
  if l==r:return a[l],l,r
  m=(l+r)//2;left=solve(l,m);right=solve(m+1,r);s=0;bestl=(-10**9,m)
  for i in range(m,l-1,-1):s+=a[i];bestl=max(bestl,(s,i))
  s=0;bestr=(-10**9,m+1)
  for i in range(m+1,r+1):s+=a[i];bestr=max(bestr,(s,i))
  cross=(bestl[0]+bestr[0],bestl[1],bestr[1]);return max(left,right,cross)
 return solve(0,len(a)-1)
if __name__=='__main__':print('Maximum sales-period gain:',max_gain([-2,1,-3,4,-1,2,1,-5,4]))
