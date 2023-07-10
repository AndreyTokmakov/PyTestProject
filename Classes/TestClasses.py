

class TestClass:
    '''
    def __init__(self):
        pass
    '''

    text: str = None

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print("\n -------> SETUP <-------")

        cls.text = "TEST"

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print("\n\n -------> TEADDOWN <-------")

    def test_one(self):
        # self.text = 'TEST'
        assert "T" in self.text

    def test_two(self):
        # self.text = 'TEST'
        assert "E" in self.text
