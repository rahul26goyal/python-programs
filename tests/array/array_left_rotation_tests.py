
import unittest

from array.array_left_rotation import rotate_using_temp_array, rotate_using_reversing_array

class TestArrayLeftRotation(unittest.TestCase):

    def test_dummy(self):
        self.assertEqual("test", "test")

    def test_empty_array(self):
        input, expected, rotate_by = [], [], 2
        result = rotate_using_temp_array(input, rotate_by)
        self.assertEqual(result, expected)

        input, expected, rotate_by = [], [], 2
        result = rotate_using_reversing_array(input, rotate_by)
        self.assertEqual(result, expected)

    def test_zero_rotation(self):
        input, expected, rotate_by = [1,2,3], [1,2,3], 0
        result = rotate_using_temp_array(input, rotate_by)
        self.assertEqual(result, expected)

        input, expected, rotate_by = [1, 2, 3], [1, 2, 3], 0
        result = rotate_using_reversing_array(input, rotate_by)
        self.assertEqual(result, expected)

    def test_rorate_by_small(self):
        input, expected, rotate_by = [1, 2, 3, 4, 5, 6], [3,4,5,6,1,2], 2
        result = rotate_using_temp_array(input, rotate_by)
        self.assertEqual(result, expected)

        input, expected, rotate_by = [1, 2, 3, 4, 5, 6], [3, 4, 5, 6, 1, 2], 2
        result = rotate_using_reversing_array(input, rotate_by)
        self.assertEqual(result, expected)

    def test_rorate_by_big_rotate(self):
        input, expected, rotate_by = [1, 2, 3, 4, 5, 6], [3, 4, 5, 6, 1, 2], 8
        result = rotate_using_temp_array(input, rotate_by)
        self.assertEqual(result, expected)

        input, expected, rotate_by = [1, 2, 3, 4, 5, 6], [3, 4, 5, 6, 1, 2], 2
        result = rotate_using_reversing_array(input, rotate_by)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
