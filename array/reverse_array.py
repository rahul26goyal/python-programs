# write a program to reverse the givem list.

def main():
    arr = []
    print("Input Array", arr)
    reverse(arr)
    print(" => Reversed", arr)

    arr = [1]
    print("Input Array", arr)
    reverse(arr)
    print(" => Reversed", arr)

    arr = [1,2,3,4]
    print("Input Array", arr)
    reverse(arr)
    print(" => Reversed", arr)

    arr = [1, 2, 3, 4, 5]
    print("Input Array", arr)
    reverse(arr)
    print(" => Reversed", arr)

    print("--------Reverse by range -------")

    arr = [1, 2, 3, 4, 5]
    print("Input Array", arr)
    reverse_by_index(arr, 0, 3)
    print(" => Reversed by range({}, {})".format(0, 3), arr)


def reverse(arr):
    if type(arr) != list:
        return arr
    size = len(arr)
    if size == 0 or size == 1:
        return arr
    return reverse_by_index(arr, 0, size-1)


# Revers the given range
def reverse_by_index(arr, start, end):
    if start > end or start < 0 or end > len(arr):
        print("expected starts < end but found otherwise {} & {}".format(start, end))
        return arr
    mid = (start + end )/ 2;
    #print("Range: ", start, "-", mid, "-", end)
    i = 0
    while start < mid:
        temp = arr[start]
        arr[start] = arr[end]
        arr[end] = temp
        start += 1
        end -= 1

    #print("arr:",arr)
    return arr


if __name__ == '__main__':
    main()

