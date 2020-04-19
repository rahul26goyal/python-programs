# implement  binary search algorithm to search an element in an array:


def binary_search(arr, ele):
    """Implementation of Binary Search Algorithms for list bases Data Structure"""
    if type(arr) != list or len(arr) == 0 or ele is None:
        return -1
    return _binary_search_impl(arr, 0, len(arr) - 1, ele)


def _binary_search_impl(arr, start, end, ele):
    """Internal Implementation"""
    print(start, end)
    if start <= end:
        mid = int(start + (end - start) / 2)
        if arr[mid] == ele:
            return mid
        elif ele < arr[mid]:
            return _binary_search_impl(arr, start, mid-1, ele)
        elif ele > arr[mid]:
            return _binary_search_impl(arr, mid + 1, end, ele)
    else:
        return -1








