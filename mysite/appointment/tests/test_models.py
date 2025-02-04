from datetime import timedelta, time

from django.test import TestCase
from django.utils import timezone

from appointment.models import Appointment
from client.models import Client
from service.models import Service
from employee.models import Employee


class AppointmentModelTest(TestCase):
    """
    Test cases for the Appointment model.

    This class contains unit tests to verify the functionality and behavior of the Appointment model in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test instances of Client, Employee, Service, and Appointment.
        """
        self.client = Client.objects.create(first_name="Juan", last_name="Perez")
        self.employee = Employee.objects.create(first_name="Maria", last_name="Leon")
        self.service1 = Service.objects.create(name="Manicura", duration=timedelta(minutes=30))
        self.service2 = Service.objects.create(name="Facial", duration=timedelta(hours=1))
        
        # Create a test appointment
        self.appointment = Appointment.objects.create(
            client=self.client,
            employee=self.employee,
            date=timezone.now().date(),
            start_time=time(10, 0)  # 10:00 AM
        )
        self.appointment.services.add(self.service1, self.service2)
    
    def test_appointment_creation(self):
        """
        Test the creation of an Appointment instance.

        Verifies that the appointment is created with the correct client and employee.
        """
        self.assertTrue(isinstance(self.appointment, Appointment))
        self.assertEqual(self.appointment.client, self.client)
        self.assertEqual(self.appointment.employee, self.employee)
    
    def test_appointment_string_representation(self):
        """
        Test the string representation of an Appointment.

        Ensures that the __str__ method returns the expected string format.

        """
        expected_string = f"Cita de {self.client} el {self.appointment.date} a las {self.appointment.start_time}"
        
        self.assertEqual(str(self.appointment), expected_string)
    
    def test_appointment_title(self):
        """
        Test the title method of an Appointment.

        Verifies that the title method returns the correct format with client name and services.
        """
        expected_title = f"Juan Perez\nFacial\n Manicura"

        self.assertEqual(self.appointment.title(), expected_title)
    
    def test_calculate_end_time(self):
        """
        Test the calculation of the appointment end time.

        Ensures that the end time is correctly calculated based on service durations.
        """
        expected_end_time = time(11, 30)  # 10:00 AM + 1h30m
        
        self.assertEqual(self.appointment.calculate_end_time().time(), expected_end_time)
    
    def test_appointment_without_employee(self):
        """
        Test creating an appointment without an assigned employee.

        Verifies that an appointment can be created with a null employee field.
        """
        appointment_without_employee = Appointment.objects.create(
            client=self.client,
            date=timezone.now().date(),
            start_time=time(14, 0)  # 2:00 PM
        )
        
        self.assertIsNone(appointment_without_employee.employee)
    
    def test_appointment_with_notes(self):
        """
        Test adding notes to an appointment.

        Ensures that notes can be added and retrieved correctly.
        """
        self.appointment.notes = "Petición especiales para la cita."
        self.appointment.save()
        
        self.assertEqual(self.appointment.notes, "Petición especiales para la cita.")
    
    def test_appointment_ordering(self):
        """
        Test the default ordering of appointments.

        Verifies that appointments are ordered by their start time.
        """
        Appointment.objects.create(
            client=self.client,
            date=timezone.now().date(),
            start_time=time(9, 0)  # 9:00 AM
        )
        
        appointments = Appointment.objects.all()
        
        self.assertEqual(appointments[0].start_time, time(9, 0))
        self.assertEqual(appointments[1].start_time, time(10, 0))
    
    def test_appointment_index(self):
        """
        Test the presence of an index on the start_time field.

        Ensures that the database index for start_time is created.
        """
        indexes = [index.fields for index in Appointment._meta.indexes]
        
        self.assertIn(['start_time'], indexes)
        