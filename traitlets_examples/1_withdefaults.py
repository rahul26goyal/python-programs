import unittest
from traitlets import default, HasTraits, Int, Unicode


class DefaultStudent(HasTraits):
    # declaring the methods types.
    student_id = Int()
    student_name = Unicode()

    def __init__(self):
        pass

    @default("student_name")
    def student_name_default(self):
        return "RahulgDefault"

    @default("student_id")
    def student_id_default(self):
        return 12345


class TestDefaultStudent(unittest.TestCase):

    def test_default(self):
        s1 = DefaultStudent()
        self.assertTrue(s1.student_id == 12345)
        self.assertTrue(s1.student_name == "RahulgDefault")
        s1.student_id = 123
        self.assertTrue(s1.student_id == 123)
