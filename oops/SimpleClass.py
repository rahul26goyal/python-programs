"""
Define a simple Dog class with fet instance variables
and instance methods.
"""
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.log = logger
        self.log.info("Created a dog object")

    # Python does not suppoprt method overloading
    # def __int__(self):
    #     super("default", "indian")

    """
    Proving an implentation for the python object to string conversion
    """

    def __str__(self):
        return f"Dog(name: {self.name}, breed: {self.breed})"

    def bark(self):
        self.log.info("Bark!!!")

    def __del__(self):
        self.log.info("Object destructor called...")


if __name__ == "__main__":
    # dog = Dog() #TypeError: __init__() missing 2 required positional arguments: 'name' and 'breed'
    jimmy = Dog("Jimmy", "Labro")
    logger.info(f"Jimmy: {jimmy}")  # prints the object.__str__()
    logger.info(f"Dog name: {jimmy.name}")
    logger.info(f"Dog name: {jimmy.breed}")
    jimmy.bark()

    jimmy.name = "HACKED!!!"  # we will look at how to prevent this later.
    logger.info(f"Jimmy: {jimmy}")  # prints the object.__str__()
