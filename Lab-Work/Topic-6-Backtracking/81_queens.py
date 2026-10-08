n=int(input());cols=[]
def solve(r):
 if r==n:print(cols);return True
 for c in range(n):
  if all(c!=x and abs(c-x)!=r-i for i,x in enumerate(cols)):
   cols.append(c+1)
   if solve(r+1):return True
   cols.pop()
 return False
solve(0)
