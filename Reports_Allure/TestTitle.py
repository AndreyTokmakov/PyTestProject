import allure
import pytest


@pytest.mark.parametrize("login", ["johndoe", "johndoe@example.com"])
@allure.title("Test Authentication (login: {login})")
def test_authentication(login):
    allure.dynamic.parameter("auth_method", "password")
    # ...


@allure.title("Test Authentication (login: empty)")
def test_authentication_with_empty_login():
    allure.dynamic.parameter("auth_method", "password")
    allure.dynamic.parameter("login", "")
