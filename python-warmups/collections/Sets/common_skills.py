student_a = {"Python", "Java", "SQL"}
student_b = {"Python", "C++", "SQL"}

common=student_a & student_b
print(common)

##another way
print(f"Common skills: {student_a.intersection(student_b)}")

##all_skills
all_skills=student_a | student_b
print(f"All skills: {all_skills}")

##skills only A have
only_A_has=student_a - student_b
print(f"Skills only A have: {only_A_has}")