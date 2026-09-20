print("1. Celsius to fahrenheit")
print("2. Fahrenheit to Celsius")

choice=int(input("Enter your choice: "))
match choice:
    case 1:
        celsius=float(input("Enter the temperature: "))
        fahrenheit=(celsius*1.8)+32
        print(f"Celsius to Fahrenheit: {fahrenheit:.1f}")
    case 2:
        fahrenheit=float(input("Enter the temperature: "))
        celsius=(fahrenheit-32)/1.8
        print(f"Fahrenheit to Celsius: {celsius:.1f}")
    case _:
        print("Enter valid number")

