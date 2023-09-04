

class TestCase(object):

    def __init__(self):
        print("* * * * * * * * * TestCase::__init__() * * * * * * * * ")
        self.value = 'TestCase'

    def info(self):
        print(f'{self.value}')
