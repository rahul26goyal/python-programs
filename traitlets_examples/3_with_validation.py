import traitlets
import unittest
from traitlets import HasTraits, Int, Unicode


class StudentValidation(HasTraits):
    student_id = Int()
    student_name = Unicode()

    def __init__(self):
        pass

    @traitlets.validate("student_id")
    def _validate_student_id(self, change_details):
        new_id = change_details["value"]  # fetch the new value
        if new_id < 1 or new_id > 100:
            raise traitlets.TraitError("Student Id out of rang(1, 100), found: {}".format(new_id))
        return new_id  # this value gets assigned to self.student_id


class TestStudentValidation(unittest.TestCase):

    def test_create_valid(self):
        stud = StudentValidation()
        stud.student_id = 12
        self.assertTrue(stud.student_id == 12)

    def test_create_invalid1(self):
        stud = StudentValidation()
        with self.assertRaises(traitlets.TraitError) as tre:
            stud.student_id = -1
        self.assertEqual(str(tre.exception), "Student Id out of rang(1, 100), found: -1")

    def test_create_invalid2(self):
        stud = StudentValidation()
        with self.assertRaises(traitlets.TraitError) as tre:
            stud.student_id = 101
        self.assertEqual(str(tre.exception), "Student Id out of rang(1, 100), found: 101")