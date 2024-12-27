"""
Sample unit test set for fizzbuzz.py.
"""

import unittest
from simple_tests.fizzbuzz import fizzbuzz
from simple_tests.point import TwoPoint
from simple_tests.quicksort import quickSort

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

class TestQuickSort(unittest.TestCase):
    def test_easy_arr(self) ->None:
        arr = [10, 7, 8, 9, 1, 5]
        arr = quickSort(arr, 0, len(arr) - 1)
        assert arr == [1, 5, 7, 8, 9, 10]
    
    def test_dupl_arr(self) ->None:
        arr = [10, 7, 8, 9, 1, 1, 1, 8, 10, 11, 5]
        arr = quickSort(arr, 0, len(arr) - 1)
        assert arr == [1, 1, 1, 5, 7, 8, 8, 9, 10, 10, 11]

    def test_identical_arr(self)->None:
        arr = [1, 1, 1, 1, 1, 1]
        arr = quickSort(arr, 0, len(arr) - 1)
        assert arr == [1, 1, 1, 1, 1, 1]

    def test_in_sorted_order(self)->None:
        arr = [1, 2, 3, 4, 5]
        arr = quickSort(arr, 0, len(arr) - 1)
        assert arr == [1, 2, 3, 4, 5]

    def test_empty_arr(self)->None:
        arr = []
        arr = quickSort(arr, 0, len(arr) - 1)
        assert arr == []

    def test_one_elem_arr(self)->None:
        arr = [5]
        arr = quickSort(arr, 0, len(arr) - 1)
        assert arr == [5]


if __name__ == "__main__":
    unittest.main()
