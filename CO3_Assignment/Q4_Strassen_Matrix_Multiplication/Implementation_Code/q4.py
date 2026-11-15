def add(a,b):return [[a[i][j]+b[i][j] for j in range(len(a))]for i in range(len(a))]
def sub(a,b):return [[a[i][j]-b[i][j] for j in range(len(a))]for i in range(len(a))]
def mul(a,b):
 n=len(a);return [[sum(a[i][k]*b[k][j]for k in range(n))for j in range(n)]for i in range(n)]
def strassen(a,b):
 n=len(a)
 if n==1:return [[a[0][0]*b[0][0]]]
 h=n//2; A,B=[[r[:h]for r in a[:h]],[r[h:]for r in a[:h]],[r[:h]for r in a[h:]],[r[h:]for r in a[h:]]],[[r[:h]for r in b[:h]],[r[h:]for r in b[:h]],[r[:h]for r in b[h:]],[r[h:]for r in b[h:]]]
 a11,a12,a21,a22=A;b11,b12,b21,b22=B
 m1=strassen(add(a11,a22),add(b11,b22));m2=strassen(add(a21,a22),b11);m3=strassen(a11,sub(b12,b22));m4=strassen(a22,sub(b21,b11));m5=strassen(add(a11,a12),b22);m6=strassen(sub(a21,a11),add(b11,b12));m7=strassen(sub(a12,a22),add(b21,b22))
 c11=add(sub(add(m1,m4),m5),m7);c12=add(m3,m5);c21=add(m2,m4);c22=add(sub(add(m1,m3),m2),m6)
 return [c11[i]+c12[i]for i in range(h)]+[c21[i]+c22[i]for i in range(h)]
if __name__=='__main__':
 a=[[1,7],[3,5]];b=[[1,3],[7,5]];print('Strassen:',strassen(a,b));print('Conventional:',mul(a,b))
