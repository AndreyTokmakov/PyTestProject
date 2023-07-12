import pytest


@pytest.mark.parametrize("num, expected", [(1, 2), (2, 4), (3, 6), (4, 8)])
def test_mult_two(num, expected):
    assert 2 * num == expected
