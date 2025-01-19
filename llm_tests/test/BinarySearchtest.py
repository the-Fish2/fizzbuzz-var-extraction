import unittest
from llm_tests.code.BinarySearch import binarysearch

class TestBinarySearch(unittest.TestCase):
    def test_found_element(self):
        arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        target = 23
        self.assertEqual(binarysearch(arr, target), 5)

    def test_not_found_element(self):
        arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        target = 10
        self.assertEqual(binarysearch(arr, target), -1)

    def test_empty_array(self):
        arr = []
        target = 10
        self.assertEqual(binarysearch(arr, target), -1)

    def test_single_element_array_found(self):
        arr = [10]
        target = 10
        self.assertEqual(binarysearch(arr, target), 0)

    def test_single_element_array_not_found(self):
        arr = [10]
        target = 20
        self.assertEqual(binarysearch(arr, target), -1)

    def test_array_with_duplicates(self):
        arr = [2, 5, 8, 12, 16, 23, 23, 38, 56, 72, 91]
        target = 23
        self.assertEqual(binarysearch(arr, target), 5)

    def test_array_with_negative_numbers(self):
        arr = [-10, -5, 0, 5, 10, 15, 20]
        target = 5
        self.assertEqual(binarysearch(arr, target), 3)

    def test_array_with_float_numbers(self):
        arr = [1.1, 2.2, 3.3, 4.4, 5.5]
        target = 3.3
        self.assertEqual(binarysearch(arr, target), 2)