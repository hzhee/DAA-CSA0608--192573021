words = input("Enter words: ").split()
answer = []

for word in words:
    for other in words:
        if word != other and word in other:
            answer.append(word)
            break

print(answer)
