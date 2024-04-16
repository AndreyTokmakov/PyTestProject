from typing import List


def add_numbers(a: int, b: int) -> int:
    return a + b


def subtract_numbers(a: int, b: int) -> int:
    return a - b


def multiply_numbers(a: int, b: int) -> int:
    return a * b


def divide_numbers(a: int, b: int) -> float:
    return a / b


def average(values: List[int]) -> float:
    return sum(values) / len(values)
