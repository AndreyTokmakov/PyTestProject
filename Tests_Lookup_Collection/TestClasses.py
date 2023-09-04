import inspect


# Enabled = Truw
def PurpleTest(cls):
    cls.__purple_test__ = True
    return cls


@PurpleTest
class PyTestClass:
    text: str = None

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print('\n', '===' * 50, '\n', '\t' * 7, 'SETUP\n', '===' * 50, '\n', sep='')
        cls.text = "TEST"

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class TeadDown\n', '===' * 50, sep='')

    def test_one(self):
        # self.text = 'TEST'
        print(f'\ntest_one\n')
        assert "T" in self.text

    def test_two(self):
        # self.text = 'TEST'
        print(f'\ntest_two\n')
        assert "E" in self.text


class PyTestClass2:

    def __init__(self):
        pass


    text: str = None

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print('\n', '===' * 50, '\n', '\t' * 7, 'SETUP\n', '===' * 50, '\n', sep='')
        cls.text = "TEST"

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class TeadDown\n', '===' * 50, sep='')

    def test_one(self):
        # self.text = 'TEST'
        print(f'\ntest_one\n')
        assert "T" in self.text

    def test_two(self):
        # self.text = 'TEST'
        print(f'\ntest_two\n')
        assert "E" in self.text
