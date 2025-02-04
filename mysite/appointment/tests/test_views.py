import json
from datetime import timedelta, date, time

from django.contrib.messages import get_messages
from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.utils import timezone

from appointment.models import Appointment
from client.models import Client
from service.models import Service, Category
from employee.models import Employee


class AppointmentCreateViewTest(TestCase):
    """
    Test cases for the AppointmentCreateView.

    This class contains unit tests to verify the functionality and behavior of the AppointmentCreateView in the
    application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test instances of Client, Category, Employee, and Services.
        """
        self.client = TestClient()
        self.url = reverse('appointment:create')
        
        self.client_model = Client.objects.create(first_name="Juan", last_name="Perez")
        self.category = Category.objects.create(name="Facial")
        self.employee = Employee.objects.create(first_name="Maria", last_name="Leon")
        self.service1 = Service.objects.create(name="Antiedad", category=self.category, duration=timedelta(hours=1))
        self.service2 = Service.objects.create(name="Express", category=self.category, duration=timedelta(minutes=30))
        self.employee.services.add(self.service1, self.service2)
    
    def test_appointment_create_GET(self):
        """
        Test the GET request to the appointment create page.

        Verifies that the page loads correctly and contains all necessary context data.
        """
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment/create.html')
        self.assertIn('form', response.context)
        self.assertIn('clients', response.context)
        self.assertIn('employees', response.context)
        self.assertIn('services_by_category', response.context)
        self.assertIn('service_durations', response.context)
    
    def test_appointment_create_with_employee(self):
        """
        Test the GET request with a pre-selected employee.

        Ensures that the view handles pre-selected employee correctly and provides appropriate service options.
        """
        response = self.client.get(f"{self.url}?employee_id={self.employee.id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['employee_id'], str(self.employee.id))
        self.assertIn(self.service1.name, response.context['service_durations'])
        self.assertIn(self.service2.name, response.context['service_durations'])
    
    def test_appointment_create_with_datetime(self):
        """
        Test the GET request with a pre-selected date and time.

        Verifies that the form is pre-populated with the provided date and time.
        """
        date_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        response = self.client.get(f"{self.url}?date={date_time}")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('date', response.context['form'].initial)
        self.assertIn('start_time', response.context['form'].initial)
    
    def test_appointment_create_POST_valid(self):
        """
        Test the POST request with valid appointment data.

        Ensures that a new appointment is created correctly when valid data is submitted.
        """
        post_data = {
            'client': self.client_model.id,
            'services': [self.service1.id],
            'employee': self.employee.id,
            'date': timezone.now().date(),
            'start_time': '10:00',
            'notes': 'Test appointment'
        }
        
        response = self.client.post(self.url, data=post_data)
        
        self.assertRedirects(response, reverse('appointment:agenda'))
        self.assertEqual(Appointment.objects.count(), 1)
        
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.client, self.client_model)
        self.assertEqual(appointment.employee, self.employee)
        self.assertEqual(list(appointment.services.all()), [self.service1])
        self.assertEqual(appointment.end_time.strftime('%H:%M'), '11:00')
    
    def test_appointment_create_POST_invalid(self):
        """
        Test the POST request with invalid appointment data.

        Verifies that appropriate error messages are displayed when invalid data is submitted.
        """
        post_data = {
            'client': '',  # Invalid: client is required
            'services': [],  # Invalid: at least one service is required
            'date': 'invalid-date',
            'start_time': 'invalid-time',
        }
        
        response = self.client.post(self.url, data=post_data)
   
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.', count=2)
        self.assertContains(response, 'Introduzca una fecha válida.')
        self.assertContains(response, 'Introduzca una hora válida.')
    
    def test_service_durations_json(self):
        """
        Test the JSON representation of service durations.

        Ensures that the service durations are correctly serialized and provided in the context.
        """
        response = self.client.get(self.url)
        service_durations = json.loads(response.context['service_durations'])
        
        self.assertEqual(service_durations[self.service1.name], 60)
        self.assertEqual(service_durations[self.service2.name], 30)


class AppointmentDetailViewTest(TestCase):
    """
    Test cases for the AppointmentDetailView.

    This class contains unit tests to verify the functionality and behavior of the AppointmentDetailView in the
    application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test instances of Client, Employee, Category, Service, and Appointment.
        """
        self.client = TestClient()
        self.client_model = Client.objects.create(first_name="Juan", last_name="Perez")
        self.employee = Employee.objects.create(first_name="Maria", last_name="Leon")
        self.category = Category.objects.create(name="Facial")
        self.service = Service.objects.create(name="Express", category=self.category, duration=timedelta(minutes=30))
        self.appointment = Appointment.objects.create(
            client=self.client_model,
            employee=self.employee,
            date="2023-01-01",
            start_time="10:00:00"
        )
        self.appointment.services.add(self.service)
        self.url = reverse('appointment:detail', args=[self.appointment.id])

    def test_appointment_detail_GET(self):
        """
        Test the GET request to the appointment detail page.

        Verifies that the page loads correctly and contains all necessary context data.
        """
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment/detail.html')
        self.assertIn('appointment', response.context)
        self.assertIn('form', response.context)
        self.assertIn('clients', response.context)
        self.assertIn('employees', response.context)
        self.assertIn('services_by_category', response.context)

    def test_appointment_detail_POST_valid(self):
        """
        Test the POST request with valid updated appointment data.

        Ensures that the appointment is updated correctly when valid data is submitted.
        """
        updated_data = {
            'client': self.client_model.id,
            'employee': self.employee.id,
            'services': [self.service.id],
            'date': '2023-01-02',
            'start_time': '11:00:00',
            'notes': 'Updated appointment'
        }
        
        response = self.client.post(self.url, data=updated_data)
        
        self.assertRedirects(response, reverse('appointment:agenda'))
        self.appointment.refresh_from_db()
        self.assertEqual(str(self.appointment.date), '2023-01-02')
        self.assertEqual(str(self.appointment.start_time), '11:00:00')

    def test_appointment_detail_POST_invalid(self):
        """
        Test the POST request with invalid appointment data.

        Verifies that appropriate error messages are displayed when invalid data is submitted.
        """
        invalid_data = {
            'client': '',
            'employee': '',
            'services': [],
            'date': 'invalid-date',
            'start_time': 'invalid-time',
        }
        
        response = self.client.post(self.url, data=invalid_data)
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Este campo es obligatorio" in str(m) for m in messages))
        self.assertTrue(any("Introduzca una fecha válida" in str(m) for m in messages))
        self.assertTrue(any("Introduzca una hora válida" in str(m) for m in messages))

    def test_appointment_detail_404(self):
        """
        Test the response for a non-existent appointment.

        Ensures that a 404 error is returned when trying to access a non-existent appointment.
        """
        url = reverse('appointment:detail', args=[99999])  # Non-existent ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
        
        
class AppointmentDeleteViewTest(TestCase):
    """
    Test cases for the AppointmentDeleteView.

    This class contains unit tests to verify the functionality and behavior of the AppointmentDeleteView in the
    application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test instances of Client, Employee, Category, Service, and Appointment.
        """
        self.client = TestClient()
        self.client_model = Client.objects.create(first_name="Juan", last_name="Perez")
        self.employee = Employee.objects.create(first_name="Maria", last_name="Leon")
        self.category = Category.objects.create(name="Facial")
        self.service = Service.objects.create(name="Express", category=self.category, duration=timedelta(minutes=30))
        self.appointment = Appointment.objects.create(
            client=self.client_model,
            employee=self.employee,
            date="2023-01-01",
            start_time="10:00:00"
        )
        self.appointment.services.add(self.service)
        self.url = reverse('appointment:delete', args=[self.appointment.id])

    def test_appointment_delete_GET(self):
        """
        Test the GET request to the appointment delete page.

        Verifies that the page loads correctly and contains the appointment in the context.
        """
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment/delete.html')
        self.assertIn('appointment', response.context)

    def test_appointment_delete_POST(self):
        """
        Test the POST request to delete an appointment.

        Ensures that the appointment is deleted and the user is redirected to the agenda.
        """
        response = self.client.post(self.url)
        
        self.assertRedirects(response, reverse('appointment:agenda'))
        self.assertEqual(Appointment.objects.count(), 0)

    def test_appointment_delete_404(self):
        """
        Test the response for a non-existent appointment.

        Ensures that a 404 error is returned when trying to delete a non-existent appointment.
        """
        url = reverse('appointment:delete', args=[99999])  # Non-existent ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)

    def test_appointment_delete_GET_shows_correct_appointment(self):
        """
        Test that the correct appointment is shown on the delete confirmation page.

        Verifies that the appointment in the context matches the one being deleted.
        """
        response = self.client.get(self.url)
        
        self.assertEqual(response.context['appointment'], self.appointment)

    def test_appointment_delete_POST_actually_deletes(self):
        """
        Test that the POST request actually deletes the appointment from the database.

        Ensures that the appointment no longer exists in the database after deletion.
        """
        self.client.post(self.url)
        
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=self.appointment.id)


class CalendarViewTest(TestCase):
    """
    Test cases for the CalendarView.

    This class contains unit tests to verify the functionality and behavior of the CalendarView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test instances of Client, Employees, Category, Service, and Appointments.
        """
        self.client_model = Client.objects.create(first_name="Juan", last_name="Perez")
        self.employee1 = Employee.objects.create(
            first_name="Maria",
            last_name="Leon",
            telephone_number=695321478,
            color="#FF0000")
        self.employee2 = Employee.objects.create(
            first_name="Julia",
            last_name="Garcia",
            telephone_number=658412018,
            color="#00FF00")
        self.category = Category.objects.create(name="Facial", color="#0000FF")
        self.service = Service.objects.create(name="Express", category=self.category, duration=timedelta(minutes=30))
      
        self.appointment1 = Appointment.objects.create(
            client=self.client_model,
            employee=self.employee1,
            date=date(2023, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0)
        )
        self.appointment1.services.add(self.service)
        
        self.appointment_without_service = Appointment.objects.create(
            client=self.client_model,
            employee=self.employee2,
            date=date(2023, 1, 2),
            start_time=time(14, 0),
            end_time=time(15, 0)
        )
        
        self.url = reverse('appointment:agenda')
    
    def test_calendar_view_GET(self):
        """
        Test the GET request to the calendar view page.

        Verifies that the page loads correctly and uses the correct template.
        """
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment/agenda.html')
    
    def test_calendar_view_context(self):
        """
        Test the context data of the calendar view.

        Ensures that the necessary context variables are present.
        """
        response = self.client.get(self.url)
        
        self.assertIn('appointments_data', response.context)
        self.assertIn('column_width', response.context)
        self.assertIn('employees', response.context)
    
    def test_calendar_view_appointments_data(self):
        """
        Test the appointments data in the calendar view.

        Verifies that the appointments data is correctly formatted and contains all necessary information.
        """
        response = self.client.get(self.url)
        appointments_data = json.loads(response.context['appointments_data'])
        
        self.assertEqual(len(appointments_data), 2)  # Two employees
        
        # Find the date for employee1
        employee1_data = next((data for data in appointments_data if data['employee_id'] == self.employee1.id), None)
        self.assertIsNotNone(employee1_data)
        self.assertEqual(len(employee1_data['appointments']), 1)
        
        # Check appointment details
        appointment = employee1_data['appointments'][0]
        self.assertEqual(appointment['id'], self.appointment1.id)
        self.assertEqual(appointment['start'], '2023-01-01T10:00:00')
        self.assertEqual(appointment['end'], '2023-01-01T11:00:00')
        expected_services = f"{self.client_model.first_name} {self.client_model.last_name}\n{self.service.name}"
        self.assertEqual(appointment['extendedProps']['services'], expected_services)
        self.assertEqual(appointment['extendedProps']['employeeColor'], '#FF0000')
        self.assertEqual(appointment['extendedProps']['categoryColor'], '#0000FF')
    
    def test_calendar_view_column_width(self):
        """
        Test the calculation of column width in the calendar view.

        Ensures that the column width is correctly calculated based on the number of employees.
        """
        response = self.client.get(self.url)
        
        self.assertEqual(response.context['column_width'], 50)  # 100 / 2 employees
    
    def test_calendar_view_no_employees(self):
        """
        Test the calendar view when there are no employees.

        Verifies that the view handles the case of no employees correctly.
        """
        Employee.objects.all().delete()
        response = self.client.get(self.url)
        
        self.assertEqual(response.context['column_width'], 100)
        self.assertEqual(json.loads(response.context['appointments_data']), [])
    
    def test_calendar_view_appointment_without_services(self):
        """
        Test the display of appointments without services.

        Ensures that appointments without services are correctly represented in the calendar view.
        """
        response = self.client.get(self.url)
        appointments_data = json.loads(response.context['appointments_data'])
        
        appointment_without_service = None
        for employee_data in appointments_data:
            for appointment in employee_data['appointments']:
                if appointment['id'] == self.appointment_without_service.id:
                    appointment_without_service = appointment
                    break
            if appointment_without_service:
                break
        
        self.assertIsNotNone(appointment_without_service, "No se encontró la cita sin servicios")
        self.assertEqual(appointment_without_service['extendedProps']['services'], 'Sin tratamiento')