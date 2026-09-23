students = {
    "A": 85,
    "B": 42,
    "C": 76,
    "D": 35
}

std={name: score for name, score in students.items() if score>50}
print(std)