items=["apple", "banana", "apple", "cherry", "banana", "apple"]

hashmap={}

for word in items:
    hashmap[word]=hashmap.get(word,0)+1

print(hashmap)