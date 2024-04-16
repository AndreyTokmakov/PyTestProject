import pytest
# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parents[1]))

from calculator import (
    add_numbers,
    average,
    subtract_numbers,
    multiply_numbers,
    divide_numbers
)


# https://dev.to/cwprogram/testing-and-refactoring-with-pytest-and-pytest-cov-22d6

def test_add():
    assert add_numbers(2, 3) == 5


def test_subtract():
    assert subtract_numbers(0, 3) == -3
    assert subtract_numbers(5, 3) == 2


def test_multiply():
    assert multiply_numbers(3, 0) == 0
    assert multiply_numbers(2, 3) == 6
    assert multiply_numbers(-3, 3) == -9

'''
def test_divide():
    assert divide_numbers(6, 3) == 2.0
    with pytest.raises(ZeroDivisionError):
        divide_numbers(3, 0)


def test_average():
    assert average([90, 88, 99, 100]) == 94.25
'''