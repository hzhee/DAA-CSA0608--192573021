def merge_sort(a):
    if len(a)<2:return a
    m=len(a)//2; l,r=merge_sort(a[:m]),merge_sort(a[m:]); out=[];i=j=0
    while i<len(l) and j<len(r):
        if l[i]<=r[j]:out.append(l[i]);i+=1
        else:out.append(r[j]);j+=1
    return out+l[i:]+r[j:]
def quick_sort(a,first=True,depth=1,trace=None):
    trace=[] if trace is None else trace
    if len(a)<2:return a,depth,trace
    p=a[0] if first else a[len(a)//2]; lo=[x for i,x in enumerate(a) if i!=(0 if first else len(a)//2) and x<=p]; hi=[x for i,x in enumerate(a) if i!=(0 if first else len(a)//2) and x>p]
    trace.append((len(lo),len(hi))); l,dl,_=quick_sort(lo,first,depth+1,trace);h,dh,_=quick_sort(hi,first,depth+1,trace)
    return l+[p]+h,max(depth,dl,dh),trace
if __name__=='__main__':
    a=[42,17,63,8,55,29]; print('Merge:',merge_sort(a)); print('Quick median:',quick_sort(a,False)); print('Quick first ordered:',quick_sort(list(range(1,9)),True))
