class Product:
    def __init__(self, name, price, quantity):
        self.name=name
        self.price=price
        self.quantity=quantity

    def calculate_total(self):
        return self.price*self.quantity

product1=Product("Shampoo", 250, 2)
product2=Product("Jeans", 1500, 3)

print(product1.calculate_total())
print(product2.calculate_total())