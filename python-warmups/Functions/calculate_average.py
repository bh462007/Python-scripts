def calculate_average(marks):
    result=sum(marks)/len(marks)
    return result

marks=[67,89,92,87,56,71]
result=calculate_average(marks)
print(f"Calculated average of all the marks: {result}")