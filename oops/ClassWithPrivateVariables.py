"""
“Private” instance variables that cannot be accessed except from inside an object don’t exist in Python. However,
there is a convention that is followed by most Python code: a name prefixed with an underscore (e.g. _spam)
 should be treated as a non-public part of the API (whether it is a function, a method or a data member).

 https://docs.python.org/3/tutorial/classes.html#private-variables

"""

import logging
import random
import sys
import typing

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Dog:
    # class variables
    DOG_OBJECT_STORE = []

    # this is not an instance variable but a class variable unless
    # we create a shadow using self in class costructor
    age: int = 0

    def __init__(self, name: str, breed: str) -> any:
        self._name = name
        self._breed = breed  # protected variable syntax
        self.log = logger
        self.log.info("Created a dog object")
        self.DOG_OBJECT_STORE.append(self)
        # this creates an instance variable for this object which is different from
        # age defined as class variable.
        self.age = int(random.randint(1, 5))
        self.__origin = "indian"  ## private variable syntax which will not be available to inherited class.

    # Python does not suppoprt method overloading
    # https://realpython.com/python-multiple-constructors/#defining-multiple-class-constructors
    # def __int__(self):
    #     super("default", "indian")

    """
    Proving an implentation for the python object to string conversion
    """

    def __str__(self):
        return (
            f"Dog(name: {self._name}, breed: {self._breed}): "
            f"age: {self.age}, classLevelAge: {Dog.age}"
        )

    def bark(self):
        self.log.info("Bark!!!")

    @classmethod
    def print_classname(cls):  # takes one positional args
        logger.info(f"Class name: {cls.__class__.__name__}")

    @staticmethod
    def print_store_details():  # does not accept any defalt arg
        print("#" * 20)
        logger.info(f"Num Dogs: {len(Dog.DOG_OBJECT_STORE)}")
        logger.info(f"Dogs: {Dog.DOG_OBJECT_STORE}")
        for dog in Dog.DOG_OBJECT_STORE:
            print(f"Dog: {dog}")
        print("*" * 20)


if __name__ == "__main__":
    tommy = Dog("Tommy", "xyz")
    logger.info(tommy)

    # print(f"tommy: {tommy.name}")  # this will throw exceptipn
    print(f"tommy name: {tommy._name}")
    print(f"Origin::: {tommy._Dog__origin}")  # accessing the dunger variable
