# Write a program to calculate sum of all numbers present in a list.


def main():
    array = [1.5, 2, 3, 4, 5, 6, 7, 8, 9, "10.5", "invalid", {}, [], ()]
    #array = []
    if len(array) == 0:
        print("Empty array: Sum =", 0)
        return
    sum = 0
    for num in array:
        if type(num) == str:
            try:
                num = float(num)
            except ValueError:
                num = 0
        print("num:", num, ":" ,type(num))
        if type(num) in [int, float]:
            sum += num
    print("Result: Sum of Number: ", sum)



if __name__ == "__main__":
    print("start running main()")
    main()
else:
    print("Being imported..")