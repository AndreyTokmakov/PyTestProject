import time
from modules.TestCase import TestCase


class PyTestBaseClass:

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class SetUP\n', '===' * 50, '\n', sep='')

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class TeadDown\n', '===' * 50, sep='')

    def setup_method(self, method):
        print(f"\tsetup_method(). Called before: {method}")
        pass

    def teardown_method(self, method):
        print("\n\tteardown_method()\n")
        pass

    def test_one(self):
        time.sleep(0.5)
        test_case: TestCase = TestCase()
        test_case.info()

