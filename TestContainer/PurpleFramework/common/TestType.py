from enum import Enum, auto


class TestType(Enum):
    TestSuite = auto()
    TestCase = auto()

    def __str__(self):
        return str(self.name)
