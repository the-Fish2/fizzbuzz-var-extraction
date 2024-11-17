"""
Sample unit test set for fizzbuzz.py.
"""

import unittest
from tests.fizzbuzz import fizzbuzz
from tests.point import TwoPoint # type: ignore

class TestFizzBuzz(unittest.TestCase):
    def test_fizz(self) -> None:
        for i in [3, 6, 9]:
            assert fizzbuzz(i) == "Fizz"

    def test_buzz(self) -> None:
        for i in [10, 20, 35]:
            assert fizzbuzz(i) == "Buzz"

    def test_fizzbuzz(self) -> None:
        for i in [15, 90, 150]:
            assert fizzbuzz(i) == "FizzBuzz"


class TestGeneralFizzBuzz(unittest.TestCase):
    def test_fizz(self) -> None:
        for i in [1, 2, 4, 7, 8, 394]:
            assert fizzbuzz(i) == str(i)

class TestCustomRepresentation(unittest.TestCase):
    def test_custom_representation(self) -> None:
        z = TwoPoint()
        z.x1 = 3
        z.changeValue(17)
        assert z.x1 == 17


if __name__ == "__main__":
    unittest.main()
