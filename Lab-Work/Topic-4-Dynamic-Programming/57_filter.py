words=input().split(); prefix=input(); suffix=input(); print(max((i for i,w in enumerate(words) if w.startswith(prefix) and w.endswith(suffix)),default=-1))
