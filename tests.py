import unittest
from fizzbuzz import fizzbuzz

#Generating test cases! Checking for both different classes of tests and different functions within each test
class TestFizzBuzz(unittest.TestCase):
    def test_fizz(self):
        for i in [3, 6, 9]:
            assert fizzbuzz(i) == "Fizz"
    
    def test_buzz(self):
        for i in [10, 20, 35]:
            assert fizzbuzz(i) == "Buzz"

    def test_fizzbuzz(self):
        for i in [15, 90, 150]:
            assert fizzbuzz(i) == "FizzBuzz"


class TestGeneralFizzBuzz(unittest.TestCase):
    def test_fizz(self):
        for i in [1, 2, 4, 7, 8, 394]:
            assert fizzbuzz(i) == i


if __name__ == '__main__':
    unittest.main()