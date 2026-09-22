class Rectangle:
    def __init__(self, length, width):
        self.length=length
        self.width=width
    def area(self):
        return self.length*self.width
        
    def perimeter(self):
        return 2*(self.length + self.width)

t1=Rectangle(67,34)
t2=Rectangle(34,56)

print("========Area=======")
print(t1.area())
print(t2.area())

print("++++++Perimeter++++++")
print(t1.perimeter())
print(t2.perimeter())