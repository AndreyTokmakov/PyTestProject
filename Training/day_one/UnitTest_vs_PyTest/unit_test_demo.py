import unittest

from BankAccount import BankAccount


class BankAccountTest(unittest.TestCase):

    def test_insufficient_balance(self):
        acct =  BankAccount(1)
        acct.deposit(200)
        outcome: bool = acct.withdraw(300)

        self.assertFalse(outcome)

    def test_negative_balance(self):
        acct =  BankAccount(1)
        # acct.deposit(200)
        outcome: bool = acct.deposit(-300)

        self.assertFalse(outcome)
