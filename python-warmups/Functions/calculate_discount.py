def calculate_discount(price, discount_percentage):
    discount=price*(discount_percentage/100)
    final_price=price-discount
    return final_price

price=float(input("Enter the price: "))
discount_percentage=int(input("Enter discount percentage(%): "))

print(f"Final price will be {calculate_discount(price, discount_percentage)}")