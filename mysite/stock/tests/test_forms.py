from decimal import Decimal

from django import forms
from django.test import TestCase

from stock.forms import ProductForm, StockMovementForm
from stock.models import Supplier, Product, StockMovement


# Test ProductForm
class ProductFormTest(TestCase):
    """
    Test cases for the ProductForm.

    This class contains unit tests to verify the functionality and validation of the ProductForm in the application.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.

        Creates a test supplier for use in all test methods.
        """
        cls.supplier = Supplier.objects.create(name="Test Supplier")

    def test_product_form_valid_data(self):
        """
        Test that the form is valid when provided with correct data.
        """
        form_data = {
            'name': 'Test Product',
            'supplier': self.supplier.id,
            'description': 'Test Description',
            'price': Decimal('10.99'),
            'stock': 100
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_form_invalid_data(self):
        """
        Test that the form is invalid when provided with incorrect data.
        
        Verifies that validation errors are raised for missing or invalid fields.
        """
        form_data = {
            'name': '',  # Name is required
            'supplier': '',  # Supplier is required
            'description': 'Test Description',  # Optional, no error expected here
            'price': 'not a number',  # Invalid price
            'stock': -1  # Stock can't be negative
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('stock', form.errors)

    def test_product_form_empty_supplier_label(self):
        """
        Test that the "supplier" field has the correct empty label.
        """
        form = ProductForm()
        self.assertEqual(form.fields['supplier'].empty_label, "Selecciona un proveedor")

    def test_product_form_widgets(self):
        """
        Test that the form fields use the correct widget types.
        """
        form = ProductForm()
        self.assertIsInstance(form.fields['name'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['supplier'].widget, forms.Select)
        self.assertIsInstance(form.fields['description'].widget, forms.Textarea)
        self.assertIsInstance(form.fields['price'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['stock'].widget, forms.NumberInput)

    def test_product_form_widget_attrs(self):
        """
        Test that the form fields have the correct widget attributes, such as CSS classes.
        """
        form = ProductForm()
        self.assertEqual(form.fields['name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 3)


# Test StockMovementForm
class StockMovementFormTest(TestCase):
    """
    Test cases for the StockMovementForm.

    This class contains unit tests to verify the functionality and validation of the StockMovementForm in the application.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.

        Creates a test product and supplier for use in all test methods.
        """
        supplier = Supplier.objects.create(name="Test Supplier")
        cls.product = Product.objects.create(
            name="Test Product",
            supplier=supplier,
            price=Decimal('10.99'),
            stock=100
        )

    def test_stock_movement_form_valid_data(self):
        """
        Test that the form is valid when provided with correct data.
        """
        form_data = {
            'quantity': 10,
            'movement_type': 'increase',
            'reason': 'increase stock'
        }
        form = StockMovementForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_stock_movement_form_invalid_data(self):
        """
        Test that the form is invalid when provided with incorrect data.
        
        Verifies that validation errors are raised for invalid fields, such as non-numeric quantities or invalid
        movement types.
        """
        form_data = {
            'quantity': 'not a number',
            'movement_type': 'invalid',
            'reason': 'invalid'
        }
        form = StockMovementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_stock_movement_form_widgets(self):
        """
        Test that the form fields use the correct widget types.
        """
        form = StockMovementForm()
        self.assertIsInstance(form.fields['quantity'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['movement_type'].widget, forms.Select)
        self.assertIsInstance(form.fields['reason'].widget, forms.Select)

    def test_stock_movement_form_widget_attrs(self):
        """
        Test that the form fields have the correct widget attributes, such as CSS classes.
        """
        form = StockMovementForm()
        self.assertEqual(form.fields['quantity'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['movement_type'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['reason'].widget.attrs['class'], 'form-control')