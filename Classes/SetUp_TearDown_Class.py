import time


class TestClassBlahBlahBlah:

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class SetUP\n', '===' * 50, '\n', sep='')

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class TeadDown\n', '===' * 50, sep='')

    def test_one(self):
        time.sleep(0.5)
