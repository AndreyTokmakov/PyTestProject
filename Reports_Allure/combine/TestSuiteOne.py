import pytest
import allure


@allure.title("ARP Poisoning")
@allure.description("This test attempts to log into the website using a login and a password. Fails if any error happens.\n\n"
                    "Note that this test does not test 2-Factor Authentication.")
@allure.tag("security", "regression", "attack")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "John Doe")
@allure.link("https://en.wikipedia.org/wiki/ARP_spoofing", name="ARP spoofing")   # Some other Link
# @allure.issue("https://ssrc.atlassian.net/browse/PT-115")  # BUG Link
@allure.testcase("https://ssrc.atlassian.net/browse/PT-115", "PT-115: ARP cache poisoning")
# @allure.parent_suite("Some_Parent_Suite")
@allure.suite('SecurityTests')
def test_arp_poisoning():
    print('test_arp_poisoning()')
    pass

