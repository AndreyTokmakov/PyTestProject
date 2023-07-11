import pytest


@pytest.fixture
def even_number():
    return 2


@pytest.fixture
def odd_number():
    return 1


def is_even(number: int) -> bool:
    return 0 == number % 2


def test_valid_even(even_number):
    value = even_number
    assert is_even(value)


def test_invalid_even(odd_number):
    value = odd_number
    assert is_even(value)
