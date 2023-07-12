import pytest

from Palindrome import is_palindrome


@pytest.mark.parametrize("string, result", [
    ('', True),
    ('a', True),
    ('aa', True),
    ('abcba', True),
    ('abccba', True),
    ('ab', False),
    ('00 1 00', True),
    ('!@##@!', True),
])
def test_mult_two(string, result: bool):
    assert is_palindrome(string) == result
