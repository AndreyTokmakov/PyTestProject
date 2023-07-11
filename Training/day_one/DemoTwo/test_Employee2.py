from Training.day_one.DemoTwo.ClassesUnderTests import Employee


class Test_Employee:

    @classmethod
    def setup_class(cls):
        # print("*** ONCE FOR CLASS***")
        pass

    def setup_method(self):
        self.empl: Employee = Employee("Jonh", "Dow", 10_000.0)
        # print("*** ONCE FOR METHOD***")

    def test_employee_email(self):
        assert "Jonh.Dow@gmail.com" == self.empl.get_email()

    def test_employee_full_name(self):
        assert "Jonh Dow" == self.empl.get_full_name()

    def test_employee_pay_rise(self):

        assert 10_000 == self.empl.salary
        self.empl.apply_pay_raise()
        assert 10_500 == self.empl.salary



