n=int(input());cols=[]
def go(r):
 if r==n:
  for c in cols:print('.'*c+'Q'+'.'*(n-c-1))
  return True
 for c in range(n):
  if all(c!=x and abs(c-x)!=r-i for i,x in enumerate(cols)):cols.append(c);ok=go(r+1);cols.pop();return ok
go(0)
