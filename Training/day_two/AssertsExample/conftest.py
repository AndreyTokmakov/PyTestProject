from Reading import SpeedReading


def pytest_assertrepr_compare(op, left, right):
    print("\n\n**************************\n\n")
    if isinstance(left, SpeedReading) and isinstance(right, SpeedReading) and op == "==":
        return [
            f"Comparing instances: {left.speed} and {right.speed}"
        ]
