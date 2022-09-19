import unittest

from array.rotated_sorted_array_search import find_pivot


class TestRotatedArraySearch(unittest.TestCase):
    def test_find_pivot(self):
        input, expected, start, end = [3, 4, 5, 6, 1, 2], 3, 0, 5
        result = find_pivot(input, start, end)
        self.assertEqual(result, expected)

        input, expected, start, end = (
            [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            5,
            0,
            5,
        )
        result = find_pivot(input, start, end)
        self.assertEqual(expected, result)
