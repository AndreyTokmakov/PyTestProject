import pytest
import allure


@allure.title("Deauthentication Attack")
@allure.description("This test attempts to log into the website using a login and a password. Fails if any error happens.\n\nNote that this test does not test 2-Factor Authentication.")
@allure.tag("security", "regression", "attack")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "John Doe")
@allure.link("https://dev.example.com/", name="Website")
@allure.issue("PT-102")
@allure.testcase("TMS-456")
# @allure.parent_suite("Some_Parent_Suite")
@allure.suite('SecurityTests')
def test_deauth_attack():
    print('test_deauth_attack()')
    pass

