b=[list(input()) for _ in range(9)]
def go():
 for r in range(9):
  for c in range(9):
   if b[r][c]=='.':
    for x in '123456789':
     if x not in b[r] and all(b[i][c]!=x for i in range(9)) and all(b[i][j]!=x for i in range(r//3*3,r//3*3+3) for j in range(c//3*3,c//3*3+3)):
      b[r][c]=x
      if go():return True
      b[r][c]='.'
    return False
 return True
go();print(*[''.join(x) for x in b],sep='\n')
