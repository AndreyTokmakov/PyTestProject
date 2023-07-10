

import pytest

from Training.DemoTwo.ClassesUnderTests import Employee


class Test_Employee:

    def test_employee_email(self):
        empl: Employee = Employee("Jonh", "Dow", 10_000.0)
        assert "Jonh.Dow@gmail.com" == empl.get_email()

    def test_employee_full_name(self):
        empl: Employee = Employee("Jonh", "Dow", 10_000.0)
        assert "Jonh Dow" == empl.get_full_name()

    def test_employee_pay_rise(self):
        empl: Employee = Employee("Jonh", "Dow", 10_000.0)

        assert 10_000 == empl.salary
        empl.apply_pay_raise()
        assert 10_500 == empl.salary



