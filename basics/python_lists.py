
def run_lists():
    print("Learning python list..")

    sample_list = [1, 2, 3, "four"]
    print("Initial list: ", sample_list)
    print("Initial size: %d" % len(sample_list))

    sample_list.append(6)
    sample_list.insert(4, "FIVE")

    print("new list: ", sample_list)
    print("New size: %d" % len(sample_list))

    # pop from end
    sample_list.pop()
    print("new list: ", sample_list)
    print("New size: %d" % len(sample_list))

    # remove exact element.
    sample_list.remove(3)
    print("new list: ", sample_list)
    print("New size: %d" % len(sample_list))

    sample_list.copy()


if __name__ == '__main__':
    run_lists()