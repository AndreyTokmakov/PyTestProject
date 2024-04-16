# https://habr.com/ru/articles/513432/
import allure
import pytest


def setup():
    print("*** Setup ***")


def teardown():
    print("*** Teardown ***")


def setup_module(module):
    print("*** setup (Module) ***")


def teardown_module(module):
    print("*** teardown (Module) ***")


def setup_function(function):
    print("*** setup (Function) ***")


def teardown_function(function):
    print("*** teardown (Function) ***")


@allure.feature('Random dog')
@allure.story('Получение фото случайной собаки и вложенные друг в друга шаги')
def test_one():
    assert 'foo'.upper() == 'FOO'

# pytest --alluredir=<path to report directory> test.py