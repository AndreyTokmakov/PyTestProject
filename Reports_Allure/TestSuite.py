import pytest
import allure


@allure.title("Test Authentication")
@allure.description("This test attempts to log into the website using a login and a password. Fails if any error happens.\n\nNote that this test does not test 2-Factor Authentication.")
@allure.tag("NewUI", "Essentials", "Authentication")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "John Doe")
@allure.link("https://dev.example.com/", name="Website")
@allure.issue("AUTH-123")
@allure.testcase("TMS-456")
def test_authentication():
    print('test_authentication()')
    pass


def test1():
    print('test1()')
    pass


def test2():
    print('test2()')
    pass


def test3():
    print('test3()')
    pass


def test4():
    print('test4()')
    pass


def test5():
    print('test5()')
    pass
