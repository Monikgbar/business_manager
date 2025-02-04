from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from stock.models import Supplier, Product


class SupplierModelTest(TestCase):
    """
    Test cases for the Supplier models.

    This class contains unit tests to verify the functionality and integrity of the Supplier model in the application.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.

        Creates a test supplier for use in all test methods.
        """
        cls.supplier = Supplier.objects.create(name="Test Supplier")

    def test_supplier_creation(self):
        """
        Test the creation of a Supplier instance.

        Verifies that the supplier is created correctly and its string representation is as expected.
        """
        self.assertTrue(isinstance(self.supplier, Supplier))
        self.assertEqual(str(self.supplier), "Test Supplier")

    def test_name_max_length(self):
        """
        Test the maximum length of the supplier name field.
        """
        max_length = self.supplier._meta.get_field('name').max_length
        self.assertEqual(max_length, 250)

    def test_supplier_verbose_name(self):
        """
        Test the verbose name of the Supplier model.
        """
        self.assertEqual(self.supplier._meta.verbose_name, "proveedor")

    def test_supplier_verbose_name_plural(self):
        """
        Test the plural verbose name of the Supplier model.
        """
        self.assertEqual(self.supplier._meta.verbose_name_plural, "proveedores")

    def test_supplier_ordering(self):
        """
        Test the default ordering of Supplier instances.
        """
        self.assertEqual(self.supplier._meta.ordering, ["name"])


class ProductModelTest(TestCase):
    """
    Test cases for the Product models.
    
    This class contains unit tests to verify the functionality and integrity of the Product model in the application.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.

        Creates a test supplier and product for use in all test methods.
        """
        cls.supplier = Supplier.objects.create(name="Test Supplier")
        cls.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            supplier=cls.supplier,
            price=Decimal('10.99'),
            stock=100
        )

    def test_product_creation(self):
        """
        Test the creation of a Product instance.

        Verifies that the product is created correctly and its string representation is as expected.
        """
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), "Test Product")

    def test_name_max_length(self):
        """
        Test the maximum length of the product name field.
        """
        max_length = self.product._meta.get_field('name').max_length
        self.assertEqual(max_length, 250)

    def test_description_blank_null(self):
        """
        Test that the description field can be blank and null.
        """
        field = self.product._meta.get_field('description')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_supplier_relationship(self):
        """
        Test the foreign key relationship between Product and Supplier.
        """
        self.assertEqual(self.product.supplier, self.supplier)

    def test_price_decimal_places(self):
        """
        Test the decimal places and max digits of the price field.
        """
        max_digits = self.product._meta.get_field('price').max_digits
        decimal_places = self.product._meta.get_field('price').decimal_places
        self.assertEqual(max_digits, 10)
        self.assertEqual(decimal_places, 2)

    def test_stock_default(self):
        """
        Test the default value of the stock field.
        """
        default = self.product._meta.get_field('stock').default
        self.assertEqual(default, 0)

    def test_update_at_auto_now(self):
        """
        Test that the update_at field is automatically set to the current time.
        """
        self.assertTrue(self.product._meta.get_field('update_at').auto_now)

    def test_product_verbose_name(self):
        """
        Test the verbose name of the Product model.
        """
        self.assertEqual(self.product._meta.verbose_name, "producto")

    def test_product_ordering(self):
        """
        Test the default ordering of Product instances.
        """
        self.assertEqual(self.product._meta.ordering, ["name"])

    def test_negative_stock(self):
        """
        Test that a ValidationError is raised when trying to set a negative stock value.
        """
        with self.assertRaises(ValidationError):
            product = Product(name="Negative Stock", stock=-1)
            product.full_clean()

    def test_negative_price(self):
        """
        Test that a ValidationError is raised when trying to set a negative price.1983
        """
        with self.assertRaises(ValidationError):
            product = Product(name="Negative Price", price=Decimal('-10.00'))
            product.full_clean()