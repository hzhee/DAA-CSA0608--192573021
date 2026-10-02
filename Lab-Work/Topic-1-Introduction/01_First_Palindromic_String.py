n = int(input("Enter total number of words: "))

l = []

for i in range(n):
    word = input("Enter the word: ")
    l.append(word)

for word in l:
    if word == word[::-1]:
        print(word, "is the first palindromic string")
        break
