from typing import List

# https://realpython.com/python-with-statement/


class SimpleContext(object):
    some_value: int
    some_list: List[int]

    def __init__(self, value):
        print(f"Initializing : {self.__class__.__name__}")
        self.some_value = value

    def add_element(self, ele):
        print(f"Adding ele: {ele} to the list===========")
        self.some_list.append(ele)

    def display(self):
        print(f"some_valur : {self.some_value}, List: {self.some_list}")

    # Implementing the Context Manager hooks

    def pre_hook(self):
        print("Executing pre-hooks for the object.")
        self.some_list = []

    def post_hook(self):
        print("Executing the post hooks for the object.")
        self.some_list = []

    def __enter__(self):
        print("Enter the with statement: {}", self)
        self.pre_hook()
        return self  # must return the variable to be used is `as VAL`

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Exiting the with statement. {exc_type}, {exc_val}, {exc_tb}")
        self.post_hook()
        # return False # do not swallow exception
        # return True  # swallow exception


if __name__ == "__main__":
    print("Simple Example to test PEP-343 (with statement)")
    with SimpleContext(123) as obj:
        obj.add_element(12)
        # raise Exception("Some error")
        obj.add_element(13)
        obj.display()
