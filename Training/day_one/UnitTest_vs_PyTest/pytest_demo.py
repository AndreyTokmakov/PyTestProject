import pytest

from BankAccount import BankAccount


def test_insufficient_balance():
    acct = BankAccount(1)
    acct.deposit(200)
    outcome: bool = acct.withdraw(300)

    # self.assertFalse(outcome)
    assert False == outcome, "The outcome should be False"


def test_negative_balance():
    acct = BankAccount(1)
    # acct.deposit(200)
    outcome: bool = acct.deposit(-300)

    assert False == outcome, "The outcome should be False"


