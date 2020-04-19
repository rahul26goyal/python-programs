# Write a function rotate(ar[], d, n) that rotates arr[] of size n by d elements.

from array.reverse_array import reverse_by_index

def main():
    print("test anything..")


def rotate_using_temp_array(elements, rotate_by):
    if not valid_inputs(elements, rotate_by):
        return elements
    size = len(elements)
    rotate_by = rotate_by % size

    temp_list = []
    for i in range(0, rotate_by):
        temp_list.append(elements[i])

    for i in range(0, size-rotate_by):
        elements[i]  = elements[i + rotate_by]

    start = size-rotate_by
    for i in range(0, rotate_by):
        elements[start + i] = temp_list[i]
    return elements


def rotate_using_reversing_array(elements, rotate_by):
    if not valid_inputs(elements, rotate_by):
        return elements
    size = len(elements)
    rotate_by = rotate_by % size
    reverse_by_index(elements, 0, rotate_by-1)
    reverse_by_index(elements, rotate_by, size-1)
    reverse_by_index(elements, 0, size-1)
    return elements


def rotate_using_block_swap_algorithm(elements, rotate_by):
    if not valid_inputs(elements, rotate_by):
        return elements
    size = len(elements)
    rotate_by = rotate_by % size
    # TODO : need to understand the algorithm better to code it.





def valid_inputs(elements, rotate_by):
    if type(elements) != list:
        return False
    size = len(elements)
    if size == 0 or rotate_by == 0 or size == rotate_by:
        return False
    return True


if __name__ == '__main__':
    main()