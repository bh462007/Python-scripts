class BankAccount():
    def __init__(self, account_holder, balance):
        self.account_holder=account_holder
        self.balance=balance
    
    def deposit(self, amount):
        if amount>0:
            self.balance+=amount
            print(f"Successfully deposited ${amount}")
        else:
            print(f"Deposit amount must be positive")

    def withdraw(self, amount):
        if amount<=self.balance and amount>0:
            self.balance-=amount
            print(f"Successfully withdrawn money")
        else:
            print(f"Amount must be less than balance")

    def display_balance(self):
        return f"Total balance is {self.balance}"

user1=BankAccount("sam",58000)
user2=BankAccount("vedu", 58500)

user1.deposit(5000)
print(user1.display_balance())

user2.withdraw(500)
print(user2.display_balance())