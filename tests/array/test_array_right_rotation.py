
import unittest

from array.array_right_rotation import right_rotation_using_temp, right_rotation_using_reverse

class TestArrayRightRotation(unittest.TestCase):

    def test_empty_array(self):
        input, expected, rotate_by = [], [], 2
        result = right_rotation_using_temp(input, rotate_by)
        self.assertEqual(result, expected)

        input, expected, rotate_by = [], [], 2
        result = right_rotation_using_reverse(input, rotate_by)
        self.assertEqual(result, expected)

    def test_zero_rotation(self):
        input, expected, rotate_by = [1,2,3], [1,2,3], 0
        result = right_rotation_using_temp(input, rotate_by)
        self.assertEqual(result, expected)

        input, expected, rotate_by = [1, 2, 3], [1, 2, 3], 0
        result = right_rotation_using_reverse(input, rotate_by)
        self.assertEqual(result, expected)

    def test_rorate_by_small(self):
        input, expected, rotate_by = [1, 2, 3, 4, 5, 6], [5,6,1,2,3,4], 2
        result = right_rotation_using_temp(input, rotate_by)
        self.assertEqual(result, expected)

        input, expected, rotate_by = [1, 2, 3, 4, 5, 6], [5, 6, 1, 2, 3, 4], 2
        result = right_rotation_using_reverse(input, rotate_by)
        self.assertEqual(result, expected)

    def test_rorate_by_big_rotate(self):
        input, expected, rotate_by = [1, 2, 3, 4, 5, 6], [5,6,1,2,3,4], 8
        result = right_rotation_using_temp(input, rotate_by)
        self.assertEqual(result, expected)

        input, expected, rotate_by = [1, 2, 3, 4, 5, 6], [5, 6, 1, 2, 3, 4], 8
        result = right_rotation_using_reverse(input, rotate_by)
        self.assertEqual(result, expected)
