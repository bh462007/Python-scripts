class User:
    def __init__(self, name, email):
        self.name=name
        self.email=email
    def display_info(self):
        print(f"Users name is {self.name}")
        print(f"Users email is {self.email}")

user1=User("Samiksha", "sampawar@gmail.com")
user2=User("Vedaswi", "vedaswipatil@gmail.com")

user1.display_info()
user2.display_info()