import unittest

from array.reverse_array import reverse, reverse_by_index


class TestReverseArray(unittest.TestCase):
    def test_emmpty_array(self):
        input, expected = [], []
        result = reverse(input)
        self.assertEqual(expected, result)

    def test_size_1_array(self):
        input, expected = [1], [1]
        result = reverse(input)
        self.assertEqual(expected, result)

    def test_size_even_array(self):
        input, expected = [1, 2, 3, 4], [4, 3, 2, 1]
        result = reverse(input)
        self.assertEqual(expected, result)

    def test_size_odd_array(self):
        input, expected = [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]
        result = reverse(input)
        self.assertEqual(expected, result)

    def test_valid_range(self):
        input, expected, start, end = [1, 2, 3, 4, 5, 6], [4, 3, 2, 1, 5, 6], 0, 3
        result = reverse_by_index(input, start, end)
        self.assertEqual(expected, result)

    def test_zero_range(self):
        input, expected, start, end = [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], 0, 0
        result = reverse_by_index(input, start, end)
        self.assertEqual(expected, result)

    def test_invalid_range(self):
        input, expected, start, end = [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], 0, 10
        result = reverse_by_index(input, start, end)
        self.assertEqual(expected, result)

        input, expected, start, end = [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], -2, 2
        result = reverse_by_index(input, start, end)
        self.assertEqual(expected, result)

        input, expected, start, end = [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], 5, 0
        result = reverse_by_index(input, start, end)
        self.assertEqual(expected, result)
