codes=dict(part.split(':') for part in input().split());bits=input();out='';cur=''
for bit in bits:
 cur+=bit
 if cur in codes:out+=codes[cur];cur=''
print(out)
