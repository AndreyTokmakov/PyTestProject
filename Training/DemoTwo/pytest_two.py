import pytest

from Training.DemoTwo.ClassesUnderTests import Employee


def test_method_one():
    empl: Employee = Employee("Jonh", "Dow", 10_000.0)
    print(empl)


