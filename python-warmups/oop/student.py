class Student:
    def __init__(self, name, marks):
        self.name=name
        self.marks=marks
    
    def calculate_average(self, marks):
        average=sum(marks)/ len(marks)
        return average

    def is_passed(self, marks):
        if sum(marks)>=375:
            return f"Pass"
        else:
            return f"Fail"

student1=Student("Daksh", 78)
student2=Student("Yoshi", 89)

print("++++++++Average marks++++++++")
print(student1.calculate_average([89,78,90,84,71]))
print(student2.calculate_average([90,78,69,70,71]))

print("\n=========Finals=========")
print(student1.is_passed([89,78,90,84,71]))
print(student2.is_passed([90,78,69,70,71]))
