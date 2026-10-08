n=int(input()); blocked={tuple(map(int,x.split(','))) for x in input().split()};cols=[]
def go(r):
 if r==n:print(cols);return True
 for c in range(n):
  if (r+1,c+1) not in blocked and all(c!=x and abs(c-x)!=r-i for i,x in enumerate(cols)):cols.append(c);ok=go(r+1);cols.pop();return ok
go(0)
