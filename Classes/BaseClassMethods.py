# content of test_class.py
import time


class TestClass:

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print("setup_class()\n")

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print("teardown_class()\n")

    def setup_method(self, method):
        print(f"\tsetup_method(). Called before: {method}")
        pass

    def teardown_method(self, method):
        print("\n\tteardown_method()\n")
        pass

    def test_one(self):
        time.sleep(0.5)
        self.text = 'TEST'
        assert "T" in self.text

    def test_two(self):
        self.text = 'TEST'
        assert "E" in self.text

    def foo(self):
        self.text = 'TEST'
        assert "E" in self.text
