

class BankAccount(object):

    def __init__(self, id: int) -> None:
        self.id: int = id
        self.balance: int = 0

    def withdraw(self, amount: int) -> bool:
        if self.balance > amount:
            self.balance -= amount
            return True
        return False

    def deposit(self, amount: int) -> bool:
        self.balance += amount
        return True

