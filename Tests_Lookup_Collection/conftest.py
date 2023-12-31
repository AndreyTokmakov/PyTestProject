import copy
import inspect
from typing import List

import pytest
from _pytest.reports import CollectReport
from _pytest.nodes import Item
from _pytest.python import Class, hasinit


class CTestFile:

    def __init__(self, path, parent):
        pass


def pytest_collectstart(collector):
    """
    Collector starts collecting.
    """

    print(f'\n------> pytest_collectstart:  {collector}  {type(collector)} ******\n')
    if isinstance(collector, Class) and hasinit(collector.obj):
        print('collector if CLASS and it has __INIT__')
        collector.__dict__['__test__'] = False
        # return []


def pytest_collect_file(parent, path):
    """
    A hook into py.test to collect test_*.c test files.
    """
    print(f'\n* * * * * pytest_collect_file * * * *: {path}\n')
    if path.ext == ".c" and path.basename.startswith("test_"):
        return CTestFile(path, parent)


def pytest_collection_modifyitems(session, config, items: List[Item]):
    print(f'\n* * * * * pytest_collection_modifyitems * * * *: {config}\n')
    for item in items:
        if "interface" in item.nodeid:
            item.add_marker(pytest.mark.interface)
        elif "event" in item.nodeid:
            item.add_marker(pytest.mark.event)

        if "test_two" in item.nodeid:
            print(f"\t\t-----> Running test {item.nodeid} <-------")

    # items.clear()


def pytest_collectreport(report: CollectReport):
    """
    hook is called after a test collection has been completed, and allows us to access  the results of the collection.
    We can use this hook to inspect the collected tests, or to report any errors or warnings that occurred during collection.
    """

    '''
    if report.result:
        result_copy = copy.copy(report.result)
        report.result.clear()
        for item in result_copy:
            if 'TestClass2' not in str(item):
                report.result.append(item)

    if 'TestClass2' in str(report.nodeid):
        print('====== TestClass-2 =====')
    '''

    print(f'\n****** pytest_collectreport:  {report} {type(report)} ******')
    print('\n\t\t\tresult  :', report.result)
    print('\n\t\t\tnodeid  :', report.nodeid)
    print('\n\t\t\tfspath  :', report.fspath)
    print('\n\t\t\tlocation:', report.location)


def pytest_itemcollected(item: Item):
    """
    A hook that called for each collected node
    Just for reporting ??
    """

    print('\n', '===' * 50, '\n', '\t' * 7, 'pytest_itemcollected\n', '===' * 50, '\n', sep='')
    print(f'\npytest_itemcollected* * * *: {item.name} {item.location} {item.fspath}\n')

    print(item.parent, type(item.parent))
    if isinstance(item.parent, Class):
        print('Parent if CLASS')

    print('\n', '===' * 50, '\n')
    pass


def pytest_pycollect_makeitem(collector, name, obj):
    # print(f'\nMakeitem: {collector} {name} {obj}\n')
    if inspect.isclass(obj) and hasattr(obj, "__purple_test__") and True == obj.__purple_test__:

        print('\t\tTest class to run:', obj)
        return pytest.Class.from_parent(parent=collector, name=name, obj=obj)
    else:
        return None


def pytest_load_initial_conftests(early_config, parser, args):
    print("\npytest_load_initial_conftests() called\n")
    # Load an additional plugin module called "my_plugin"
    early_config.pluginmanager.register(name="my_plugin", module="my_plugin")


'''
# @pytest.hookimpl(hookwrapper=True)
def pytest_pycollect_makeitem(collector, name, obj):
    # print(f'\n* * * * * pytest_pycollect_makeitem * * * *: {name}\n')
    # outcome = yield
    # res = outcome.get_result()
    if inspect.isclass(obj) and obj.__name__ != "AtsClass" and hasattr(obj, "__ATS_TEST_CLASS__") and obj.__ATS_TEST_CLASS__ == 1:
        print("WE HAVE FOUND OUR CLASS")
        return pytest.Class(name, parent=collector)
        # outcome.force_result(pytest.Class(name, parent=collector))
    if inspect.isfunction(obj) and hasattr(obj, "__ATS_TEST_CLASS__") and obj.__ATS_TEST_CLASS__ == 1:
        print("WE HAVE FOUND OUR FUNCTION")
        return pytest.Function(name, parent=collector)
        # outcome.force_result([pytest.Function(name, parent=collector)])
'''
