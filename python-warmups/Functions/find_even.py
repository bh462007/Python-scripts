def is_even(num):
    if num%2==0:
        return "Even"
    return "Odd"

num=int(input("Enter a number: "))
print(f"The number {num} is {is_even(num)}")