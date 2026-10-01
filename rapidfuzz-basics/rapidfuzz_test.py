from rapidfuzz import fuzz, process

# Score:
# 0    → completely different
# 50   → somewhat similar
# 78   → fairly similar
# 100  → exactly the same

score=fuzz.ratio("ABC Limited", "ABC Ltd")

print(score)

score1=fuzz.ratio("ABC Limited", "XYZ Pvt Ltd")
print(score1)

socre2=fuzz.token_sort_ratio("ABC Ltd Nashik", "Nashik ABC Ltd")
print(socre2)

vendors=[
    "ABC Ltd",
    "XYZ Pvt Ltd",
    "ABC Limited Nashik"
]

payment_vendor="ABC Limited"

result= process.extractOne(payment_vendor, vendors, scorer=fuzz.token_sort_ratio)
print(result)