"""
This is a sample test runner using test cases for i to run the fizzbuzz function, testing all the different cases.
"""

import unittest
from fizzbuzz_funcs.fizzbuzz import fizzbuzz


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


if __name__ == "__main__":
    unittest.main()
