# Write a program to calculate sum of all numbers present in a list.


def sum_of_array(array):
    """Given an array of integers and float, returns the sum of all elements."""
    if type(array) != list or len(array) == 0:
        return 0
    result = 0
    for num in array:
        if type(num) == str:
            try:
                num = float(num)
            except ValueError:
                num = 0
        if type(num) in [int, float]:
            result += num
    return result