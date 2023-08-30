import time
import testing.mysqld

from sqlalchemy import create_engine

'''
MYSQLD_FACTORY = None


def setup_module(module):
    print(f"*** setup_module {module} ***")
    global MYSQLD_FACTORY
    MYSQLD_FACTORY = testing.mysqld.MysqldFactory(cache_initialized_db=True, port=7531)


def teardown_module(module):
    print(f"*** teardown_module {module} ***")
    global MYSQLD_FACTORY
    MYSQLD_FACTORY.clear_cache()
'''


class TestClass:

    mysqld = None

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print("setup_class()\n")
        cls.mysqld = testing.mysqld.Mysqld(my_cnf={'skip-networking': None})

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print("teardown_class()\n")
        cls.mysqld.stop()

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
