
class Person(object):

    def __init__(self,
                 person_name,
                 family_name,
                 job_title) -> None:
        self.person_name = person_name
        self.family_name = family_name
        self.job_title = job_title

    def __repr__(self):
        return f'Person({self.person_name} {self.family_name}, Job: {self.job_title})'

    # def __str__(self):
    #   return f'{self.person_name} {self.family_name}, {self.job_title}'

    def format(self) -> str:
        return f'{self.person_name} {self.family_name}, {self.job_title}'

    def to_cv_format(self) -> str:
        return f'{self.person_name},{self.family_name},{self.job_title}'
