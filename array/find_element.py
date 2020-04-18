# Write a program to check if an integer element is present in the list


def main():
    elements = [1,5,3,4,7,8,9]
    print(get_index_of(1, {}))
    print(get_index_of(1, []))
    print(get_index_of(10, elements))
    print(get_index_of(9, elements))
    print(get_index_of("9", elements))


def get_index_of(x, numbers):

    if type(numbers) == list:
        index = -1
        for num in numbers:
            index += 1
            if num == x:
                return index
        return -1
    else:
        print("Given store is not a list.")
        return -1


if __name__ == '__main__':
    main()



