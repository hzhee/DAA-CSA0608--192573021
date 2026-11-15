from itertools import combinations
def median5(a,k):
 if len(a)<=5:return sorted(a)[k]
 meds=[sorted(a[i:i+5])[len(a[i:i+5])//2]for i in range(0,len(a),5)];p=median5(meds,len(meds)//2);lo=[x for x in a if x<p];eq=[x for x in a if x==p];hi=[x for x in a if x>p]
 return median5(lo,k) if k<len(lo) else p if k<len(lo)+len(eq) else median5(hi,k-len(lo)-len(eq))
def mitm(nums,target):
 m=len(nums)//2;l=nums[:m];r=nums[m:];ls=[sum(c)for q in range(len(l)+1)for c in combinations(l,q)];rs={sum(c)for q in range(len(r)+1)for c in combinations(r,q)}
 return any(target-x in rs for x in ls),len(ls),len(rs)
if __name__=='__main__':print('4th smallest:',median5([9,1,8,2,7,3,6,4,5],3));print('MITM:',mitm([3,34,4,12,5,2],9))
