import pytest


def test_raise_zero_div_exception():
    with pytest.raises(ZeroDivisionError):
        var = 1 / 0


def test_raise_zero_div_exception_Fail():
    with pytest.raises(ZeroDivisionError):
        var = 1 / 1
