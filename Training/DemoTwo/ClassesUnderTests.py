
class Employee(object):

    theRaise: float = 1.05

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 salary: float):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.salary: float = salary

    def get_email(self) -> str:
        return f'{self.first_name}.{self.last_name}@gmail.com'

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def apply_pay_raise(self):
        self.salary *= self.theRaise

    def __repr__(self):
        return f'Employee({self.first_name} {self.last_name}, Salary: {self.salary})'
