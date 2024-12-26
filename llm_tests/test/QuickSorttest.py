import unittest
from code.QuickSort import quicksort

class TestQuickSort(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(quicksort([]), [])

    def test_single_element_array(self):
        self.assertEqual(quicksort([5]), [5])

    def test_already_sorted_array(self):
        self.assertEqual(quicksort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_unsorted_array(self):
        self.assertEqual(quicksort([3, 6, 8, 10, 1, 2, 1]), [1, 1, 2, 3, 6, 8, 10])

    def test_array_with_duplicates(self):
        self.assertEqual(quicksort([4, 2, 9, 6, 5, 1, 8, 3, 7, 5, 6]), [1, 2, 3, 4, 5, 5, 6, 6, 7, 8, 9])

    def test_array_with_negative_numbers(self):
        self.assertEqual(quicksort([3, -6, 8, -10, 1, 2, 1]), [-10, -6, 1, 1, 2, 3, 8])

    def test_array_with_zero(self):
        self.assertEqual(quicksort([3, 0, 8, 10, 1, 2, 1]), [0, 1, 1, 2, 3, 8, 10])