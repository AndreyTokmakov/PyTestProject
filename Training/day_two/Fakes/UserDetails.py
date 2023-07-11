

class User(object):

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 job: str,
                 address):
        self.first_name = first_name
        self.last_name = last_name
        self.job = job
        self.address = address

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def user_job(self):
        return f'{self.name} is a: {self.job}'

    @property
    def user_address(self):
        return f'{self.name} lives in: {self.address}'

    def __repr__(self):
        return f'User({self.first_name} {self.last_name}, Job: {self.job}, Address: {self.address})'


if __name__ == '__main__':
    user: User = User("Jonh", "McClane", "Policeman", "New York")
    print(user)
