def count_vowels(text):
    
    count=0
    for ch in text.lower().strip():
        if ch=='a' or ch=='e' or ch=='i' or ch=='o' or ch=='u':
            count=count+1
    return count

text="Hey, this is CS50 Harward class"
print(f"Total number of vowels are {count_vowels(text)}")