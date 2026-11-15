from math import hypot
def closest(points):
 p=sorted(points)
 def go(p):
  if len(p)<=3:return min((hypot(x[0]-y[0],x[1]-y[1]),x,y)for i,x in enumerate(p)for y in p[i+1:])
  m=len(p)//2;x=p[m][0];dl=go(p[:m]);dr=go(p[m:]);d=min(dl,dr);strip=sorted((q for q in p if abs(q[0]-x)<d[0]),key=lambda q:q[1])
  for i,q in enumerate(strip):
   for r in strip[i+1:i+8]:d=min(d,(hypot(q[0]-r[0],q[1]-r[1]),q,r))
  return d
 return go(p)
if __name__=='__main__': print('Closest:',closest([(2,3),(12,30),(40,50),(5,1),(12,10),(3,4)]))
