"""
Extend the Dog class to demostrate the power of
class variables and methods.
also introduct to static methods concept.

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
        self.name = name
        self.breed = breed
        self.log = logger
        self.log.info("Created a dog object")
        self.DOG_OBJECT_STORE.append(self)
        # this creates an instance variable for this object which is different from
        # age defined as class variable.
        self.age = int(random.randint(1, 5))

    # Python does not suppoprt method overloading
    # https://realpython.com/python-multiple-constructors/#defining-multiple-class-constructors
    # def __int__(self):
    #     super("default", "indian")

    """
    Proving an implentation for the python object to string conversion
    """

    def __str__(self):
        return (
            f"Dog(name: {self.name}, breed: {self.breed}): "
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
    # explore class methods and variables
    Dog.print_classname()
    Dog.print_store_details()
    # create 2 objecjs for test
    jimmy = Dog("Jimmy", "Labro")
    jimmy3 = Dog("Jimmy3", "Labross")

    # changing the value of class variable does not affect the instance variable
    # though the name is same.
    Dog.age = 100

    # print details
    Dog.print_store_details()
    # override the class values.
    logger.info("Overriding the store to empty array")
    Dog.DOG_OBJECT_STORE = []  # how to prevent this???
    Dog.print_store_details()
    logger.info(f"Dog age: {Dog.age}")
