from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from service.models import Category, Service, Voucher


# Test Category models
class CategoryModelTest(TestCase):
    """
    Test cases for the Category model.

    This class contains unit tests to verify the functionality and integrity of the Category model in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a sample Category object for use in tests.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")

    def test_category_creation(self):
        """
        Test the creation of a Category instance.

        Verifies that the created object is an instance of Category and its string representation is correct.
        """
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), "Test Category")

    def test_category_unique_name(self):
        """
        Test the uniqueness constraint on the name field.

        Ensures that creating a Category with a duplicate name raises an exception (either IntegrityError or
        ValidationError).
        """
        with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
            Category.objects.create(name="Test Category")

    def test_category_default_color(self):
        """
        Test the default color assignment for a Category.

        Verifies that when no color is specified, the default color is applied.
        """
        category = Category.objects.create(name="Default Color Category")
        self.assertEqual(category.color, "#ffffff")
        

# Test Service models
class ServiceModelTest(TestCase):
    """
    Test cases for the Service model.

    This class contains unit tests to verify the functionality and integrity of the Service model in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a sample Category and Service object for use in tests.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.service = Service.objects.create(
            name="Test Service",
            duration=timedelta(hours=1),
            price=50.00,
            category=self.category,
            available=Service.Available.POSITIVE
        )

    def test_service_creation(self):
        """
         Test the creation of a Service instance.

        Verifies that the created object is an instance of Service and its string representation is correct.
        """
        self.assertTrue(isinstance(self.service, Service))
        self.assertEqual(str(self.service), "Test Service")

    def test_service_color_property(self):
        """
        Test the color property of a Service.

        Ensures that the color property returns the color of the associated category.
        """
        self.assertEqual(self.service.color, "#123456")

    def test_service_color_property_no_category(self):
        """
        Test the color property of a Service without a category.

        Verifies that the default color is returned when the service has no associated category.
        """
        service = Service.objects.create(name="No Category Service", duration=timedelta(minutes=30))
        
        self.assertEqual(service.color, "#ffffff")

    def test_service_available_choices(self):
        """
        Test the available choices for a Service.

        Ensures that the available field can be set to different choices and that these choices are correctly saved and
        retrieved.
        """
        self.assertEqual(self.service.available, Service.Available.POSITIVE)
        self.service.available = Service.Available.NEGATIVE
        self.service.save()
        self.assertEqual(self.service.available, Service.Available.NEGATIVE)


# Test Voucher models
class VoucherModelTest(TestCase):
    """
    Test cases for the Voucher model.

    This class contains unit tests to verify the functionality and integrity of the Voucher model in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a sample Service and Voucher object for use in tests.
        """
        self.service = Service.objects.create(name="Test Service", price=50.00)
        
        self.voucher = Voucher.objects.create(
            name="Test Voucher",
            total_sessions=10,
            price_session=45.00,
            discount=10
        )
        
        self.voucher.services.add(self.service)

    def test_voucher_creation(self):
        """
        Test the creation of a Voucher instance.

        Verifies that the created object is an instance of Voucher and its string representation is correct.
        """
        self.assertTrue(isinstance(self.voucher, Voucher))
        self.assertEqual(str(self.voucher), "Test Voucher")

    def test_voucher_discounted_price_calculation(self):
        """
        Test the calculation of the discounted price for a Voucher.

        Ensures that the discounted_price property correctly calculates the total price after applying the discount.
        """
        expected_price = Decimal('405.00')  # (45 * 10) * 0.9
        self.assertEqual(self.voucher.discounted_price, expected_price)

    def test_voucher_invalid_discount(self):
        """
        Test the validation of invalid discount values.

        Verifies that creating a Voucher with a discount greater than 100 raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            voucher = Voucher(name="Invalid Discount", total_sessions=5, price_session=50.00, discount=101)
            voucher.full_clean()

    def test_voucher_invalid_price(self):
        """
        Test the validation of invalid price values.

        Ensures that creating a Voucher with a price of 0 raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            voucher = Voucher(name="Invalid Price", total_sessions=5, price_session=0, discount=10)
            voucher.full_clean()

    def test_voucher_services_relationship(self):
        """
        Test the many-to-many relationship between Voucher and Service.

        Verifies that services can be associated with a voucher and retrieved correctly.
        """
        self.assertEqual(self.voucher.services.count(), 1)
        self.assertEqual(self.voucher.services.first(), self.service)