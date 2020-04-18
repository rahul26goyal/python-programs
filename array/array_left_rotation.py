# Write a function rotate(ar[], d, n) that rotates arr[] of size n by d elements.

from array.reverse_array import reverse_by_index

def main():
    print("test anything..")


def rotate_using_temp_array(elements, rotate_count):
    size = len(elements)
    if size == 0:
        return []
    if rotate_count == 0:
        return elements

    rotate_count = rotate_count % size
    print("Rotate By: ", rotate_count)

    if rotate_count == 0:
        return elements

    temp_list = []
    for i in range(0, rotate_count):
        temp_list.append(elements[i])

    for i in range(0, size-rotate_count):
        elements[i]  = elements[i + rotate_count]

    start = size-rotate_count
    for i in range(0, rotate_count):
        elements[start + i] = temp_list[i]
    return elements


def rotate_using_reversing_array(elements, rotate_by):
    size = len(elements)
    if size == 0:
        return []
    if rotate_by == 0:
        return elements

    rotate_by = rotate_by % size
    print("Rotate By: ", rotate_by)

    if rotate_by == 0:
        return
    reverse_by_index(elements, 0, rotate_by-1)
    reverse_by_index(elements, rotate_by, size-1)
    reverse_by_index(elements, 0, size-1)
    return elements


if __name__ == '__main__':
    main()