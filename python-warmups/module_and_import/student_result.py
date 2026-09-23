from student import Student 

students=[
    Student("Sam", 45, 19, "Female"),
    Student("Bhagyashree", 35, 18, "Female"),
    Student("Vedu", 43, 19, "Female"),
    Student("Akshay", 78, 20, "Male"),
    Student("Harsh", 64, 19, "Male"),
    Student("Karan", 18, 20, "Male"),
    Student("Pooja",65, 19, "Female")
]

print("+++++++++++Student list+++++++++++")
for std in students:
    print(std.display_name())
