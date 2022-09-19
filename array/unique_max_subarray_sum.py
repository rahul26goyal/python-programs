"""
You are given an array of positive integers and find a subarray containing unique elements whose sum is maximum.
nums = [4,2,4,5,6]
Ans = 17
"""


def get_max_unique_subarray_sum(input_list):
    if not isinstance(input_list, list):
        raise TypeError("Expected list as input but found :{}".format(type(input_list)))

    if len(input_list) == 0:
        return 0
    max_sum = -1
    cur_sum = 0
    cur_subarray = {}  # dict to track ele -> lastIndex
    sum_arr = []  # stores the sum till the current index

    for i in range(len(input_list)):
        sum_arr.insert(i, 0)  # initialize the list with 0 values.

    i = 0  # starting from begnning
    while i < len(input_list):
        ele = input_list[i]
        if cur_subarray.get(ele) is None:  # ele does not exist
            cur_sum += ele  # update current sum
            cur_subarray[ele] = i  # store the index
            sum_arr[i] = cur_sum  # update sum in cache.
        else:  # duplicate element encountered.
            prev_index = cur_subarray.get(ele)  # fetch previopus index
            # new sum if we consider this over the previous subarray
            cur_sum = cur_sum - sum_arr[prev_index] + ele
            cur_subarray[ele] = i  # update index of the duplicate element.
            sum_arr[i] = cur_sum  # update current sum if ele has to be included.

        if max_sum < cur_sum:  # check if max sum needs to be updated.
            max_sum = cur_sum
        i += 1  # increment the counter.
    else:
        print("done")
    return max_sum


def get_max_unique_subarray_sum_alternate(input_list):
    if not isinstance(input_list, list):
        raise TypeError("Expected list as input but found :{}".format(type(input_list)))
    input_size = len(input_list)
    if input_size == 0:
        return 0
    subarray_set = (
        set()
    )  # declare an empty set which stores the current set of unique element.
    # print(type(subarray_set))
    i = 0  # two pointers to track the current subarray index.
    j = 1
    cur_sum = input_list[i]
    max_sum = cur_sum  # to store the max subarray sum.
    subarray_set.add(input_list[i])

    while i < (input_size - 1) and j < input_size:
        ele = input_list[j]
        if ele in subarray_set:
            # print("element already exist....")
            cur_sum = cur_sum - input_list[i]
            subarray_set.remove(
                input_list[i]
            )  # remove the ith element from current subarray
            i = (
                i + 1
            )  # increment i while keep j the same..this happens until the duplicate element index is reached.
        else:
            # print("ele does not exist: ")
            subarray_set.add(ele)  # add element into the set
            cur_sum += ele  # new sum
            max_sum = max(max_sum, cur_sum)  # update new maximum sum.
            j = j + 1  # increment j pointer.
    return max_sum


if __name__ == "__main__":
    print("Result:" + str(get_max_unique_subarray_sum([])))
    print("Result:" + str(get_max_unique_subarray_sum([4, 2, 4, 5, 6])))
    print("Result:" + str(get_max_unique_subarray_sum([4, 2, 4, 5, 6, 4])))
    print("Result:" + str(get_max_unique_subarray_sum([6, 4, 5, 4, 3, 2])))
    print("Result:" + str(get_max_unique_subarray_sum([3, 4, 2, 4, 7])))
    print("Result:" + str(get_max_unique_subarray_sum([3, 4, 2, 4, 7, 7])))

    print("Result:" + str(get_max_unique_subarray_sum_alternate([])))
    print("Result:" + str(get_max_unique_subarray_sum_alternate([4, 2, 4, 5, 6])))
    print("Result:" + str(get_max_unique_subarray_sum_alternate([4, 2, 4, 5, 6, 4])))
    print("Result:" + str(get_max_unique_subarray_sum_alternate([6, 4, 5, 4, 3, 2])))
    print("Result:" + str(get_max_unique_subarray_sum_alternate([3, 4, 2, 4, 7])))
    print("Result:" + str(get_max_unique_subarray_sum_alternate([3, 4, 2, 4, 7, 7])))
    # exception case.
    print("Result:" + str(get_max_unique_subarray_sum_alternate({3, 4, 2, 4, 7, 7})))
