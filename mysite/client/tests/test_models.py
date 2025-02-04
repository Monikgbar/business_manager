from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils.timezone import now

from client.models import Client, ClientVoucher
from service.models import Voucher


# Models tests
class ClientModelTest(TestCase):
    """
    Test case for the Client model.

    This class contains tests to verify the functionality of the Client model,
    including creation, validation, and representation.
    """
    
    def setUp(self):
        """
        Set up the tests environment.

        This method creates a Client object to be used in the tests.
        """
        self.client = Client.objects.create(
            first_name="Juan",
            last_name="Perez",
            email="juan@example.com"
        )

    def test_client_creation(self):
        """
        Test the creation of a Client object.

        Verifies that the Client object is created with the correct attributes.
        """
        self.assertEqual(self.client.first_name, "Juan")
        self.assertEqual(self.client.last_name, "Perez")
        self.assertEqual(self.client.email, "juan@example.com")
        
    def test_client_str_representation(self):
        """
        Test the string representation of a Client object.

        Verifies that the __str__ method returns the expected string.
        """
        self.assertEqual(str(self.client), "Juan Perez")
    
    def test_client_with_empty_name(self):
        """
        Test client creation with empty names.

        Verifies that creating a Client with empty first and last names raises a ValidationError.
        """
        client = Client(first_name="", last_name="")
        with self.assertRaises(ValidationError):
            client.full_clean()
    
    def test_client_with_invalid_email(self):
        """
        Test client creation with an invalid email.

        Verifies that creating a Client with an invalid email address raises a ValidationError.
        """
        client = Client(first_name="Juan", last_name="Perez", email="invalid-email")
        with self.assertRaises(ValidationError):
            client.full_clean()
    
    def test_client_with_duplicate_email(self):
        """
        Test client creation with a duplicate email.

        Verifies that creating a Client with an email that already exists raises an IntegrityError.
        """
        Client.objects.create(first_name="Ana", last_name="Garcia", email="tests@example.com")
        with self.assertRaises(IntegrityError):
            Client.objects.create(first_name="Pedro", last_name="Rodriguez", email="tests@example.com")
    
    def test_client_with_valid_telephone_number(self):
        """
        Test client creation with a valid telephone number.

        Verifies that a Client can be created with a valid telephone number.
        """
        client = Client.objects.create(
            first_name="Juan",
            last_name="Perez",
            telephone_number="+1234567890"
        )
        self.assertEqual(client.telephone_number, "+1234567890")
    
    def test_client_with_invalid_telephone_number(self):
        """
        Test client creation with an invalid telephone number.

        Verifies that creating a Client with an invalid telephone number raises a ValidationError.
        """
        client = Client(first_name="Juan", last_name="Perez", telephone_number="invalid number")
        with self.assertRaises(ValidationError):
            client.full_clean()
            
    
class ClientVoucherModelTest(TestCase):
    """
    Test case for the ClientVoucher model.

    This class contains tests to verify the functionality of the ClientVoucher model,
    including creation, validation, and methods.
    """
    
    def setUp(self):
        """
        Set up the tests environment.

        This method creates Client, Voucher, and ClientVoucher objects to be used in the tests.
        """
        self.client = Client.objects.create(first_name="Juan", last_name="Perez", email="juan@example.com")
        self.voucher = Voucher.objects.create(name="Masajes", total_sessions=10)
        self.client_voucher = ClientVoucher.objects.create(
            client=self.client,
            voucher=self.voucher,
            purchase_date="2025-01-25",
            expiration_date="2025-02-24",
            sessions_remaining=10
        )
    
    def test_client_voucher_creation(self):
        """
        Test the creation of a ClientVoucher object.

        Verifies that the ClientVoucher object is created with the correct attributes.
        """
        self.assertEqual(self.client_voucher.client, self.client)
        self.assertEqual(self.client_voucher.sessions_remaining, 10)
        self.assertEqual(self.client_voucher.is_active, True)
    
    def test_client_voucher_str_representation(self):
        """
        Test the string representation of a ClientVoucher object.

        Verifies that the __str__ method returns the expected string.
        """
        self.assertEqual(
            str(self.client_voucher),
            "Juan Perez - Masajes (10 sesiones restantes)."
        )
    
   
    
   
