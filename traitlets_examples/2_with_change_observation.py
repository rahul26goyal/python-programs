import traitlets
import unittest
from traitlets import HasTraits, Int, Unicode, Dict


class EmployeeObservation(HasTraits):
    employee_id = Int()
    employee_name = Unicode
    employee_salary = Int()
    employee_address = Dict()
    change_triggered = traitlets.Bool()

    def __init__(self, e_id, e_name):
        self.employee_id = e_id
        self.employee_name = e_name
        # self.change_triggered = False # By default value set in False.

    def reset_trigger(self):
        self.change_triggered = False

    @traitlets.observe("employee_salary")
    def change_in_employee_salary(self, salary_delta):
        print("change in salary old: ", salary_delta["old"])
        print("change in salary new: ", salary_delta["new"])
        self.change_triggered = True

    @traitlets.observe("employee_id", "employee_name")
    def monitor_address_change(self, change_details):
        print("Old Data : ", change_details["old"])
        print("New Data : ", change_details["new"])
        self.change_triggered = True


class TestEmployeeObservation(unittest.TestCase):

    def test_change_salary_trigger(self):
        emp = EmployeeObservation(123, "rahul")
        self.assertFalse(emp.change_triggered)
        emp.employee_salary = 1000
        self.assertTrue(emp.change_triggered)

    def test_change_empid_trigger(self):
        emp = EmployeeObservation(123, "rahul")
        emp.reset_trigger()
        print("testing change....")
        emp.employee_id = 1222
        self.assertTrue(emp.change_triggered)