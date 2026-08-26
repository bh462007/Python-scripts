def my_decorator(func):
    def wrapper():
        print("something is happening before calling a function")
        func()
        print("something happened after function calling")
    return wrapper
    
@my_decorator
def say_hello():
    print("hello wolrd")

say_hello()