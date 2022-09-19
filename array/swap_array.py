# Write a program to swap `num` elements from the list from pos si, sj
# eg: [1,2,3,4,5,6,7], si= 1, sj = 4, num = 2
# rs: [1,5,6,4,2,3,7]


def swap_num_elements(arr, num, si, sj):
    if si >= sj or num == 0 or ((si + num) > sj):
        return arr
    if type(arr) != list or len(arr) == 0 or len(arr) < (sj + num):
        return arr

    for i in range(0, num):
        temp = arr[si + i]
        arr[si + i] = arr[sj + i]
        arr[sj + i] = temp

    # print("arr:", arr)
    return arr
