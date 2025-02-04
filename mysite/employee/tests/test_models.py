from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from employee.models import Employee
from service.models import Service


class EmployeeModelTest(TestCase):
    """
    A test case class for the Employee model.
    
    This class contains unit tests to verify the functionality and integrity of the Employee model in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a sample Employee and Service object for use in tests.
        """
        self.employee = Employee.objects.create(
            first_name="Juan",
            last_name="Perez",
            telephone_number="623456789",
            email="juan@example.com",
            color="#FF5733"
        )
        
        self.services = Service.objects.create(name="Masaje Relajante")

    def test_employee_creation(self):
        """
        Test the creation of an Employee instance.

        Verifies that the created object is an instance of Employee and its string representation is correct.
        """
        self.assertTrue(isinstance(self.employee, Employee))
        self.assertEqual(str(self.employee), "Juan Perez")

    def test_employee_fields(self):
        """
        Test the fields of the Employee model.

        Checks if all fields of the created Employee object contain the expected values.
        """
        self.assertEqual(self.employee.first_name, "Juan")
        self.assertEqual(self.employee.last_name, "Perez")
        self.assertEqual(self.employee.telephone_number, "623456789")
        self.assertEqual(self.employee.email, "juan@example.com")
        self.assertEqual(self.employee.color, "#FF5733")

    def test_employee_default_color(self):
        """
        Test the default color assignment for an Employee.

        Verifies that when no color is specified, the default color is applied.
        """
        employee = Employee.objects.create(
            first_name="Ana",
            last_name="Garcia",
            telephone_number="687654321"
        )
        
        self.assertEqual(employee.color, "#3498db")

    def test_employee_services(self):
        """
        Test the many-to-many relationship between Employee and Service.

        Checks if services can be added to an employee and retrieved correctly.
        """
        self.employee.services.add(self.services)
        self.assertEqual(self.employee.services.count(), 1)
        self.assertEqual(self.employee.services.first(), self.services)

    def test_unique_telephone_number(self):
        """
        Test the uniqueness constraint on the telephone number field.

        Ensures that creating an Employee with a duplicate telephone number raises an IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                first_name="Pedro",
                last_name="Gomez",
                telephone_number="623456789"  # Duplicate telephone number
            )

    def test_unique_email(self):
        """
        Test the uniqueness constraint on the email field.

        Ensures that creating an Employee with a duplicate email raises an IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                first_name="María",
                last_name="López",
                telephone_number="611222333",
                email="juan@example.com"  # Duplicate email
            )

    def test_invalid_telephone_number(self):
        """
        Test validation for invalid telephone numbers.

        Verifies that attempting to create an Employee with an invalid telephone number raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            employee = Employee(
                first_name="Luis",
                last_name="Martinez",
                telephone_number="invalid_number"
            )
            employee.full_clean()

    def test_optional_email(self):
        """
        Test that the email field is optional.

         Ensures an Employee can be created without specifying an email.
        """
        employee = Employee.objects.create(
            first_name="Carlos",
            last_name="Rodriguez",
            telephone_number="655666777"
        )
        
        self.assertIsNone(employee.email)

    def test_str_representation(self):
        """
        Test the string representation of an Employee object.

        Verifies that the __str__ method returns the expected string.
        """
        self.assertEqual(str(self.employee), "Juan Perez")

    def test_ordering(self):
        """
        Test the default ordering of Employee objects.

        Checks if Employees are ordered alphabetically by first name.
        """
        Employee.objects.create(
            first_name="Ana",
            last_name="Garcia",
            telephone_number="699888777"
        )
        employees = Employee.objects.all()
        
        self.assertEqual(employees[0].first_name, "Ana")
        self.assertEqual(employees[1].first_name, "Juan")