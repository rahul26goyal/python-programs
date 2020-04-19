
import unittest

from array.swap_array import swap_num_elements

class TestSwapArray(unittest.TestCase):

    def test_empty_array(self):
        input, expected, num, si, sj = [], [], 1, 0, 2
        result = swap_num_elements(input, num, si, sj)
        self.assertEqual(expected, result)

    def test_zero_swap(self):
        input, expected, num, si, sj = [1, 2, 3],  [1, 2, 3], 0, 0, 1
        result = swap_num_elements(input, num, si, sj)
        self.assertEqual(expected, result)

    def test_border_swap(self):
        input, expected, num, si, sj = [1, 2, 3, 4],  [3, 4, 1,2], 2, 0, 2
        result = swap_num_elements(input, num, si, sj)
        self.assertEqual(expected, result)

    def test_valid_range(self):
        input, expected, num, si, sj = [1, 2, 3, 4, 5, 6, 7], [1,5,6,4,2,3,7], 2, 1, 4
        result = swap_num_elements(input, num, si, sj)
        self.assertEqual(expected, result)

        input, expected, num, si, sj = [1, 2, 3, 4, 5, 6, 7], [4, 5, 6, 1, 2, 3, 7], 3, 0 , 3
        result = swap_num_elements(input, num, si, sj)
        self.assertEqual(expected, result)

    def test_out_of_range(self):
        input, expected, num, si, sj = [1, 2, 3, 4], [1, 2, 3, 4], 3, 0, 3
        result = swap_num_elements(input, num, si, sj)
        self.assertEqual(expected, result)

    def test_invalid_range(self):
        input, expected, num, si, sj = [1, 2, 3, 4], [1, 2, 3, 4], 3, 3, 0
        result = swap_num_elements(input, num, si, sj)
        self.assertEqual(expected, result)

    def test_invaid_mix_range(self):
        input, expected, num, si, sj = [1, 2, 3, 4], [1, 2, 3, 4], 2, 0, 1
        result = swap_num_elements(input, num, si, sj)
        self.assertEqual(expected, result)