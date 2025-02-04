from django import forms
from django.test import TestCase

from employee.forms import ColorInput, EmployeeForm, ServicesEmployeeForm
from employee.models import Employee
from service.models import Service


class ColorInputTest(TestCase):
    """
    A test case class for the ColorInput widget.
    """
    
    def test_color_input_type(self):
        """
        Test the input type of the ColorInput widget.

        Verifies that the input_type attribute of ColorInput is set to "color".
        """
        widget = ColorInput()
        
        self.assertEqual(widget.input_type, "color")


class EmployeeFormTest(TestCase):
    """
    A test case class for the EmployeeForm.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Initializes form data for use in tests.
        """
        self.form_data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'telephone_number': '623456789',
            'email': 'juan@example.com',
            'color': '#FF5733'
        }

    def test_employee_form_valid(self):
        """
        Test the EmployeeForm with valid data.

        Ensures that the form is valid when provided with correct data.
        """
        form = EmployeeForm(data=self.form_data)
        
        self.assertTrue(form.is_valid())

    def test_employee_form_invalid(self):
        """
        Test the EmployeeForm with invalid data.

        Verifies that the form is invalid when provided with an incorrect email, and that the appropriate error is
        raised.
        """
        invalid_data = self.form_data.copy()
        invalid_data['email'] = 'invalid-email'
        form = EmployeeForm(data=invalid_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_employee_form_widgets(self):
        """
        Test the widgets used in the EmployeeForm.

        Checks if the correct widget types are used for each form field.
        """
        form = EmployeeForm()
        
        self.assertIsInstance(form.fields['first_name'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['last_name'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['telephone_number'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['email'].widget, forms.EmailInput)
        self.assertIsInstance(form.fields['color'].widget, ColorInput)

    def test_employee_form_widget_attrs(self):
        """
        Test the attributes of widgets in the EmployeeForm.

        Verifies that the widgets have the correct CSS classes and placeholder texts.
        """
        form = EmployeeForm()
        
        self.assertEqual(form.fields['first_name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['first_name'].widget.attrs['placeholder'], 'Nombre')
        self.assertEqual(form.fields['last_name'].widget.attrs['placeholder'], 'Apellidos')
        self.assertEqual(form.fields['telephone_number'].widget.attrs['placeholder'], 'Teléfono')
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email')


class ServicesEmployeeFormTest(TestCase):
    """
    A test case class for the ServicesEmployeeForm.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates sample Employee and Service objects for use in tests.
        """
        self.employee = Employee.objects.create(
            first_name="Ana",
            last_name="Garcia",
            telephone_number="687654321"
        )
        self.service1 = Service.objects.create(name="Masaje Relajante")
        self.service2 = Service.objects.create(name="Manicura")

    def test_services_employee_form_valid(self):
        """
        Test the ServicesEmployeeForm with valid data.

        Ensures that the form is valid when provided with correct service selections.
        """
        form_data = {'services': [self.service1.id, self.service2.id]}
        form = ServicesEmployeeForm(data=form_data, instance=self.employee)
        
        self.assertTrue(form.is_valid())

    def test_services_employee_form_widget(self):
        """
        Test the widget used for the services field in ServicesEmployeeForm.

        Checks if the correct widget type (CheckboxSelectMultiple) is used for the services field.
        """
        form = ServicesEmployeeForm()
        
        self.assertIsInstance(form.fields['services'].widget, forms.CheckboxSelectMultiple)

    def test_services_employee_form_save(self):
        """
        Test saving data with the ServicesEmployeeForm.

        Verifies that selected services are correctly associated with the employee when the form is saved.
        """
        form_data = {'services': [self.service1.id, self.service2.id]}
        form = ServicesEmployeeForm(data=form_data, instance=self.employee)
        if form.is_valid():
            form.save()
            
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.services.count(), 2)
        self.assertIn(self.service1, self.employee.services.all())
        self.assertIn(self.service2, self.employee.services.all())