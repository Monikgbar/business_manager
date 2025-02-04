from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from service.forms import ServiceForm, CategoryForm, VoucherForm
from service.models import Service, Category, Voucher


class ServiceFormTest(TestCase):
    """
    Test cases for the ServiceForm.

    This class contains unit tests to verify the functionality and validation of the ServiceForm in the application.
    """
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a sample Category object for use in tests.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")

    def test_valid_service_form(self):
        """
        Test the ServiceForm with valid data.

        Ensures that the form is valid when provided with correct data for all fields.
        """
        form_data = {
            'name': 'Test Service',
            'category': self.category.id,
            'price': 50.00,
            'duration': timedelta(hours=1, minutes=30),
            'available': Service.Available.POSITIVE
        }
        form = ServiceForm(data=form_data)
        
        self.assertTrue(form.is_valid())

    def test_invalid_service_form(self):
        """
        Test the ServiceForm with invalid data.

        Verifies that the form is invalid when provided with incorrect data, and that appropriate error messages are
        generated for each invalid field.
        """
        form_data = {
            'name': '',  # Invalid: empty name
            'price': 'not a number',  # Invalid: not a number
            'duration': 'invalid',  # Invalid: wrong format
        }
        
        form = ServiceForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('duration', form.errors)

    def test_clean_duration(self):
        """
        Test the cleaning of the duration field in the ServiceForm.

        Ensures that the duration field is correctly cleaned and converted to a timedelta object when valid data is
        provided.
        """
        form_data = {
            'name': 'Test Service',
            'category': self.category.id,
            'price': 50.00,
            'duration': timedelta(hours=1, minutes=30),
            'available': Service.Available.POSITIVE
        }
        
        form = ServiceForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['duration'], timedelta(hours=1, minutes=30))


class CategoryFormTest(TestCase):
    """
    Test cases for the CategoryForm.

    This class contains unit tests to verify the functionality and validation of the CategoryForm in the application.
    """
    
    def test_valid_category_form(self):
        """
        Test the CategoryForm with valid data.

        Ensures that the form is valid when provided with correct data for all fields.
        """
        form_data = {
            'name': 'Test Category',
            'color': '#123456'
        }
        
        form = CategoryForm(data=form_data)
        
        self.assertTrue(form.is_valid())

    def test_invalid_category_form(self):
        """
        Test the CategoryForm with invalid data.

        Verifies that the form is invalid when provided with incorrect data, and that appropriate error messages are
        generated for each invalid field.
        """
        form_data = {
            'name': '',  # Invalid: empty name
            'color': 'not a color'  # Invalid: not a valid color
        }
        
        form = CategoryForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('color', form.errors)


class VoucherFormTest(TestCase):
    """
    Test cases for the VoucherForm.

    This class contains unit tests to verify the functionality and validation of the VoucherForm in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a sample Category and Service object for use in tests.
        """
        self.category = Category.objects.create(name="Test Category")
        self.service = Service.objects.create(
            name="Test Service",
            category=self.category,
            price=50.00,
            duration=timedelta(hours=1)
        )

    def test_valid_voucher_form(self):
        """
        Test the VoucherForm with valid data.

        Ensures that the form is valid when provided with correct data for all fields.
        """
        form_data = {
            'name': 'Test Voucher',
            'services': [self.service.id],
            'price_session': 45.00,
            'total_sessions': 10,
            'discount': 10
        }
        
        form = VoucherForm(data=form_data)
        
        self.assertTrue(form.is_valid())

    def test_invalid_voucher_form(self):
        """
        Test the VoucherForm with invalid data.

        Verifies that the form is invalid when provided with incorrect data, and that appropriate error messages are
        generated for each invalid field.
        Also checks for form-wide validation errors.
        """
        form_data = {
            'name': '',  # Invalid: empty name
            'price_session': 'not a number',  # Invalid: not a number
            'total_sessions': 0,  # Invalid: should be positive
            'discount': 101  # Invalid: should be between 0 and 100
        }
        
        form = VoucherForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('services', form.errors)
        self.assertIn('price_session', form.errors)
        self.assertIn('discount', form.errors)
        self.assertIn('__all__', form.errors)
