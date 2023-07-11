
from Reading import SpeedReading


def test_one():
    r1 = SpeedReading(1, "one")
    r2 = SpeedReading(1, "one")
    assert r1 == r2
