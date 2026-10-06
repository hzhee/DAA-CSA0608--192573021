s=input(); answer=''
for i in range(len(s)):
 for j in range(i+1,len(s)+1):
  if s[i:j]==s[i:j][::-1] and j-i>len(answer): answer=s[i:j]
print(answer)
