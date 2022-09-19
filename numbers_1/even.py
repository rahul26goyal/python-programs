def is_even(num):
    """Check if the given number is even or odd"""
    if type(num) != int or type(num) != float:
        return False
    return (num % 2) == 0
