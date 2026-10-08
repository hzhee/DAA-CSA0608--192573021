grid=[list(map(int,input().split()))for _ in range(int(input()))]; n=len(grid); path=[]
def solve(r,c):
    if r==n-1 and c==n-1:path.append((r,c));return True
    if not(0<=r<n and 0<=c<n) or not grid[r][c]:return False
    grid[r][c]=0;path.append((r,c));answer=solve(r+1,c)or solve(r,c+1)
    if not answer:path.pop()
    return answer
print(solve(0,0),path)
