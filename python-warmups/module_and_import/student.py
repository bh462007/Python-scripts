class Student:
    def __init__(self, name, rollno, age, gender):
        self.name=name
        self.rollno=rollno
        self.age=age
        self.gender=gender

    def display_name(self):
        return self.name

    