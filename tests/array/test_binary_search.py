import unittest

from array.binary_search import binary_search


class TestBinarySearch(unittest.TestCase):
    def test_lower_boundry(self):
        input, expected, num = [5, 10, 15, 20], 0, 5
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20, 25], 0, 5
        result = binary_search(input, num)
        self.assertEqual(expected, result)

    def test_upper_boundry(self):
        input, expected, num = [5, 10, 15, 20], 3, 20
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20, 25], 4, 25
        result = binary_search(input, num)
        self.assertEqual(expected, result)

    def test_middle_boundry(self):
        input, expected, num = [5, 10, 15, 20], 1, 10
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20], 2, 15
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20, 25], 2, 15
        result = binary_search(input, num)
        self.assertEqual(expected, result)

    def test_not_found(self):
        input, expected, num = [5, 10, 15, 20], -1, 0
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20, 25], -1, 0
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20], -1, 7
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20, 25], -1, 13
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20], -1, 50
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20, 25], -1, 50
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20], -1, 21
        result = binary_search(input, num)
        self.assertEqual(expected, result)

        input, expected, num = [5, 10, 15, 20, 25], -1, 24
        result = binary_search(input, num)
        self.assertEqual(expected, result)
