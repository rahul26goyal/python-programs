import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Person:  # every class inherits from object by default
    COUNT = 0

    def __init__(self, name):
        self._name = name
        self.__private_var = "Some Secret we dont want to pass on"
        self.log = logger
        Person.COUNT += 1  # class variable.

    def __str__(self):
        return f"Person(name: {self._name})"

    def __repr__(self):
        return f"Person({self._name})"

    def print_secret(self):
        self.log.info(f"Secret: {self.__private_var}")

    def walk(self):
        self.log.info("Walking!!!!")


class Employee(Person):
    def __init__(self, name, gender):
        # super(Dog, self).__int__(name)  # ols syntax
        super().__init__(name)
        self.gender = gender

    def __str__(self):
        return f"Employee(name: {self._name}, gender: {self.gender})"

    def walk(self):
        self.log.info("Employee")
        super(Employee, self).walk()


if __name__ == "__main__":
    person = Person("A1")
    logger.info(person)
    person.print_secret()

    jimy = Employee("Jimmy", "male")
    logger.info(f"Employee: {jimy}")
    jimy.walk()
