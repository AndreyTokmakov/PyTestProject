import pytest


@pytest.mark.webtest
class TestWeb:

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print('\n', '===' * 50, '\n', '\t' * 7, 'SETUP\n', '===' * 50, '\n', sep='')
        cls.text = "TEST"

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class TeadDown\n', '===' * 50, sep='')

    def test_startup(self):
        print('\n test_startup\n')

    def test_startup_and_more(self):
        print('\n test_startup_and_more\n')


class TestCase:

    __test__ = False

    def __init__(self):
        print('* * * TestCase * * ')
