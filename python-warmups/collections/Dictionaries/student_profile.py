student={
    "name":"Bhagya",
    "age":19,
    "branch":"computer engineering",
    "cgpa":9.09
}
for val in student.values():
    print(val)

##read
print(student["cgpa"])

##create
student["Gender"]="Female"
print(student)

##delete
del student["branch"]
print(student)