
from array.reverse_array import reverse_by_index

def right_rotation_using_temp(elements, rotate_by):
    if not valid_inputs(elements, rotate_by):
        return elements
    size = len(elements)
    rotate_by = rotate_by % size

    temp_arr = []
    for i in range(size-rotate_by, size):
        temp_arr.append(elements[i])

    end = size - 1
    start = size - rotate_by - 1
    while start >= 0:
        elements[end] = elements[start]
        end -= 1
        start -= 1
    for i in range(0, rotate_by):
        elements[i] = temp_arr[i]
    print("result {}".format(elements))
    return elements


def right_rotation_using_reverse(elements, rotate_by):
    if not valid_inputs(elements, rotate_by):
        return elements
    size = len(elements)
    rotate_by = rotate_by % size

    reverse_by_index(elements, 0, size - rotate_by -1)
    reverse_by_index(elements, size - rotate_by, size -1)
    reverse_by_index(elements, 0, size-1)
    print(elements)
    return  elements

def valid_inputs(elements, rotate_by):
    if type(elements) != list:
        return False
    size = len(elements)
    if size == 0 or rotate_by == 0 or size == rotate_by:
        return False
    return True

