def karatsuba(x,y,c=None):
    c={'mult':0} if c is None else c
    if x<10 or y<10:c['mult']+=1;return x*y,c
    n=max(len(str(x)),len(str(y))); h=n//2; p=10**h; a,b=divmod(x,p);d,e=divmod(y,p)
    ac,c=karatsuba(a,d,c); be,c=karatsuba(b,e,c); mid,c=karatsuba(a+b,d+e,c)
    return ac*p*p+(mid-ac-be)*p+be,c
if __name__=='__main__':
    x,y=12345678,87654321; z,c=karatsuba(x,y); print('Karatsuba:',z,'multiplications:',c['mult']);print('Python verification:',x*y)
