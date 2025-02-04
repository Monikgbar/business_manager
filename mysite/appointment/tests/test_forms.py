from datetime import timedelta, time

from django import forms
from django.test import TestCase
from django.utils import timezone

from appointment.forms import CreateAppointmentForm
from appointment.models import Appointment
from client.models import Client
from service.models import Service
from employee.models import Employee


class CreateAppointmentFormTest(TestCase):
    """
    Test cases for the CreateAppointmentForm.

    This class contains unit tests to verify the functionality and behavior of the CreateAppointmentForm in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test instances of Client, Employee, and Services.
        """
        self.client = Client.objects.create(first_name="Juan", last_name="Perez")
        self.employee = Employee.objects.create(first_name="Maria", last_name="Leon")
        self.service1 = Service.objects.create(name="Express", duration=timedelta(minutes=30))
        self.service2 = Service.objects.create(name="Facial", duration=timedelta(hours=1))

    def test_form_fields(self):
        """
        Test the presence and order of fields in the form.

        Verifies that all expected fields are present in the form.
        """
        form = CreateAppointmentForm()
        expected_fields = ['client', 'services', 'employee', 'date', 'start_time', 'end_time', 'notes']
        
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_form_widgets(self):
        """
        Test the widget types used for each form field.

        Ensures that appropriate widget types are used for each field.
        """
        form = CreateAppointmentForm()
        
        self.assertIsInstance(form.fields['client'].widget, forms.Select)
        self.assertIsInstance(form.fields['services'].widget, forms.SelectMultiple)
        self.assertIsInstance(form.fields['employee'].widget, forms.Select)
        self.assertIsInstance(form.fields['date'].widget, forms.DateInput)
        self.assertIsInstance(form.fields['start_time'].widget, forms.TimeInput)
        self.assertIsInstance(form.fields['end_time'].widget, forms.TimeInput)
        self.assertIsInstance(form.fields['notes'].widget, forms.Textarea)

    def test_form_valid_data(self):
        """
        Test form validation with valid data.

        Verifies that the form is valid when provided with correct data.
        """
        form_data = {
            'client': self.client.id,
            'services': [self.service1.id, self.service2.id],
            'employee': self.employee.id,
            'date': timezone.now().date(),
            'start_time': '10:00',
            'end_time': '11:30',
            'notes': 'Test appointment'
        }
        
        form = CreateAppointmentForm(data=form_data)
        
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Test form validation with invalid data.

        Ensures that the form is invalid when provided with incorrect data and that appropriate error messages are
        generated.
        """
        form_data = {
            'client': '',  # Client is required
            'services': [],  # At least one service is required
            'date': 'invalid-date',
            'start_time': 'invalid-time',
        }
        
        form = CreateAppointmentForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('client', form.errors)
        self.assertIn('services', form.errors)
        self.assertIn('date', form.errors)
        self.assertIn('start_time', form.errors)

    def test_form_save_method(self):
        """
        Test the save method of the form.

        Verifies that the form correctly creates an Appointment instance when saved with valid data.
        """
        form_data = {
            'client': self.client.id,
            'services': [self.service1.id, self.service2.id],
            'employee': self.employee.id,
            'date': timezone.now().date(),
            'start_time': '10:00',
            'end_time': '11:30',
            'notes': 'Test appointment'
        }
        
        form = CreateAppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        appointment = form.save()
        self.assertIsInstance(appointment, Appointment)
        self.assertEqual(appointment.client, self.client)
        self.assertEqual(appointment.employee, self.employee)
        self.assertEqual(list(appointment.services.all()), [self.service1, self.service2])
        self.assertEqual(appointment.notes, 'Test appointment')

    def test_form_exclude_fields(self):
        """
        Test that certain fields are excluded from the form.

        Ensures that 'created_at' and 'updated_at' fields are not present in the form.
        """
        form = CreateAppointmentForm()
        
        self.assertNotIn('created_at', form.fields)
        self.assertNotIn('updated_at', form.fields)
