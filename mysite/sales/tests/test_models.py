import time
from decimal import Decimal
from datetime import datetime

from django.test import TestCase

from sales.models import Transaction
from client.models import Client
from service.models import Service
from appointment.models import Appointment


class TransactionModelTest(TestCase):
    """
    Test cases for the Transaction model.

    This class contains unit tests to verify the functionality and behavior of the Transaction model in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test instances of Client, Service, and Appointment
        """
        self.client = Client.objects.create(first_name="Juan", last_name="Perez")
        self.service = Service.objects.create(name="Express", price=Decimal('20.00'))
        self.appointment = Appointment.objects.create(
            client=self.client,
            date=datetime.now().date(),
            start_time=datetime.now().time()
        )
    
    def test_transaction_creation(self):
        """
        Test the creation of a Transaction instance.

        Verifies that a Transaction can be created with specified attributes and that its string representation is
        correct.
        """
        transaction = Transaction.objects.create(
            appointment=self.appointment,
            client=self.client,
            total_amount=Decimal('20.00'),
            method='cash'
        )
        transaction.services.add(self.service)
        self.assertTrue(isinstance(transaction, Transaction))
        self.assertEqual(str(transaction), f"Transacción de {self.client} - {transaction.date}")
    
    def test_transaction_default_values(self):
        """
        Test the default values of a Transaction.

        Ensures that a Transaction is created with the correct default values for total_amount and payment method.
        """
        transaction = Transaction.objects.create(client=self.client)
        self.assertEqual(transaction.total_amount, Decimal('0'))
        self.assertEqual(transaction.method, 'visa')
    
    def test_transaction_payment_method_choices(self):
        """
        Test the payment method choices of a Transaction.

        Verifies that a Transaction can be created with a specific payment method.
        """
        transaction = Transaction.objects.create(client=self.client, method='cash')
        self.assertEqual(transaction.method, 'cash')
    
    def test_transaction_services_relationship(self):
        """
        Test the many-to-many relationship between Transaction and Service.

        Ensures that services can be added to a Transaction and retrieved correctly.
        """
        transaction = Transaction.objects.create(client=self.client)
        transaction.services.add(self.service)
        self.assertEqual(transaction.services.count(), 1)
        self.assertEqual(transaction.services.first(), self.service)
    
    def test_transaction_client_relationship(self):
        """
        Test the foreign key relationship between Transaction and Client.

        Verifies that a Transaction is correctly associated with a Client.
        """
        transaction = Transaction.objects.create(client=self.client)
        self.assertEqual(transaction.client, self.client)
    
    def test_transaction_appointment_relationship(self):
        """
        Test the foreign key relationship between Transaction and Appointment.

        Ensures that a Transaction can be associated with an Appointment.
        """
        transaction = Transaction.objects.create(
            appointment=self.appointment,
            client=self.client
        )
        self.assertEqual(transaction.appointment, self.appointment)
    
    def test_transaction_ordering(self):
        """
        Test the default ordering of Transactions.

        Verifies that Transactions are ordered by date in descending order.
        """
        Transaction.objects.create(client=self.client)
        time.sleep(0.1)
        Transaction.objects.create(client=self.client)
        # Fetch transactions form the database
        transactions = Transaction.objects.all()
        print([transaction.date for transaction in transactions])
        self.assertTrue(transactions[0].date > transactions[1].date)
    
    def test_transaction_indexes(self):
        """
        Test the presence of database indexes on the Transaction model.

        Ensures that the appropriate indexes are created for the date and client fields.
        """
        indexes = Transaction._meta.indexes
        self.assertTrue(any(index.fields == ['date'] for index in indexes))
        self.assertTrue(any(index.fields == ['client'] for index in indexes))