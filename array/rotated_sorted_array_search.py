

from array.binary_search import _binary_search_impl


def search_in_rotated_array(elements, num):
    """Returns index of the num in a left rotated sorted array.."""
    if type(elements) != list or len(elements) == 0 or num is None:
        return -1
    end_index = len(elements) - 1
    pivot = find_pivot(elements, 0, end_index)

    if pivot == (len(elements) - 1):
        return _binary_search_impl(elements, 0, end_index, num)

    if num == elements[pivot]:
        return pivot
    if num < elements[0]:
        _binary_search_impl(elements, pivot + 1, end_index, num)
    else:
        _binary_search_impl(elements, 0, pivot - 1, num)



def find_pivot(arr, start, end):
    """Returns the pivot index of the left rotated array: pivot index is the end index of
    first half sorted array [0...pivotInfrx...end]
    >>> find_pivot([3,4,5,6,1,2], 0, 5)
    3
    """
    if start == end:
        return start
    elif start < end:
        mid = int(start + (end- start)/2)
        if mid < end and arr[mid] > arr[mid + 1]:
            return mid
        elif mid > start and arr[mid] < arr[mid -1]:
            return mid -1

        if arr[start] > arr[mid]:
            return find_pivot(arr, start, mid - 1)
        else:
            return find_pivot(arr, mid + 1, end)

    else:
        return -1
