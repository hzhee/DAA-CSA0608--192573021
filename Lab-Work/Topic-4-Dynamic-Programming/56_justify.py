words=input().split(); width=int(input()); lines=[]
while words:
 line=[words.pop(0)]
 while words and sum(map(len,line))+len(line)+len(words[0])<=width: line.append(words.pop(0))
 lines.append(' '.join(line).ljust(width) if not words or len(line)==1 else (' '*(width-sum(map(len,line))) ).join(line))
print('\n'.join(lines))
