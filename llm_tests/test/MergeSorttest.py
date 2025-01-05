import unittest
from llm_tests.code.MergeSort import mergesort

class TestMergeSort(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(mergesort([]), [])

    def test_single_element_array(self):
        self.assertEqual(mergesort([5]), [5])

    def test_already_sorted_array(self):
        self.assertEqual(mergesort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_unsorted_array(self):
        self.assertEqual(mergesort([64, 34, 25, 12, 22, 11, 90]), [11, 12, 22, 25, 34, 64, 90])

    def test_array_with_duplicates(self):
        self.assertEqual(mergesort([4, 2, 9, 6, 5, 1, 8, 3, 7, 5, 6]), [1, 2, 3, 4, 5, 5, 6, 6, 7, 8, 9])

    def test_array_with_negative_numbers(self):
        self.assertEqual(mergesort([4, -2, 9, -6, 5, 1, 8, -3, 7]), [-6, -3, -2, 1, 4, 5, 7, 8, 9])

    def test_array_with_zero(self):
        self.assertEqual(mergesort([4, 0, 9, 6, 5, 1, 8, 3, 7]), [0, 1, 3, 4, 5, 6, 7, 8, 9])