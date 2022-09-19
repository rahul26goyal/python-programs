import unittest

import traitlets


class Student:
    def __init__(self, s_id, s_name):
        # There is not strict type check to ensure the data types of the below instance variables in python by default.
        self.studId = s_id
        self.studName = s_name


class StrictStudent(traitlets.HasTraits):
    # Here, using traitlets, we set data types for the instance variables of the class.
    studId = traitlets.Int()
    studName = traitlets.Unicode()

    # def __init__(self):
    #     pass

    def __init__(self, studentId, studentName):
        self.studId = studentId
        self.studName = studentName


class TestStrictStudent(unittest.TestCase):
    def test_default(self):
        with self.assertRaises(Exception) as cm:
            Student()
        print("exception:", cm.exception)

    def test_create(self):
        stud = StrictStudent(1, "Rahulg")
        self.assertEqual(stud.studId, 1)
        self.assertEqual(stud.studName, "Rahulg")

    def test_create_anything(self):
        with self.assertRaises(Exception) as cm:
            stud = StrictStudent(1, {"name": "RahulG"})
        ex = str(cm.exception)
        self.assertTrue(
            "The 'studName' trait of a StrictStudent instance expected "
            "a unicode string, not the dict" in ex
        )


class TestStudent(unittest.TestCase):
    def test_create(self):
        stud = Student(1, "Rahulg")
        self.assertEqual(stud.studId, 1)
        self.assertEqual(stud.studName, "Rahulg")

    def test_create_anything(self):
        stud = Student(1, {"name": "RahulG"})
        self.assertEqual(stud.studId, 1)
        self.assertTrue(isinstance(stud.studName, dict))
        self.assertEqual(stud.studName.get("name"), "RahulG")
