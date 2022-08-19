
def run():
    print("hi")
    int_value = 12
    float_value = 12.1234
    string_value = "hello there!"
    print("All Inputs: %d : %f : %s" % (int_value, float_value, string_value))

    if isinstance(int_value, int):
        print("Integer value: %d" % int_value)

    if isinstance(float_value, float):
        print("Float value: %f" % float_value)

    if isinstance(string_value, str):
        print("String value: %s" % string_value)


if __name__ == '__main__':
    run()
