
import pytest
from Calculator import add, subtract


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (1, 0, 1),
    (-1, 10, 9),
    (-1, -3, -4),
    (-2, 2, 0),
])
def test_sum(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (2, 1, 1),
    (1, 0, 1),
    (-1, 10, -11),
    (-1, -3, 2),
    (2, 2, 0),
    (3, 3, 0),
])
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected
