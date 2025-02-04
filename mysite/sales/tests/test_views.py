from datetime import timedelta
from decimal import Decimal

from django.contrib.messages import get_messages
from django.core.paginator import Page
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from appointment.models import Appointment
from client.models import Client
from sales.models import Transaction
from service.models import Service


class ClientPaymentHistoryViewTest(TestCase):
    """
    Test cases for the ClientPaymentHistoryView.

    This class contains unit tests to verify the functionality and behavior of the ClientPaymentHistoryView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test client and multiple transactions for pagination testing.
        """
        self.client_model = Client.objects.create(first_name="Juan", last_name="Perez")
        self.url = reverse('sales:client_payment_history', args=[self.client_model.id])
        
        # Create 35 transactions for pagination testing
        for i in range(35):
            Transaction.objects.create(
                client=self.client_model,
                total_amount=100,
                date=timezone.now() - timedelta(days=i)
            )
    
    def test_view_url_exists_at_desired_location(self):
        """
        Test that the view is accessible at the expected URL.
        """
        response = self.client.get(f'/sales/client-payment-history/{self.client_model.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """
        Test that the view is accessible using its name in URL reversing.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """
        Test that the view uses the correct template for rendering.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales/client_payment_history.html')
    
    def test_pagination_is_thirty(self):
        """
        Test that pagination is working and displays 30 items per page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('payments' in response.context)
        self.assertTrue(len(response.context['payments']) == 30)
    
    def test_lists_all_transactions(self):
        """
        Test that all transactions are listed across multiple pages.
        """
        # Get second page and confirm it has (exactly) remaining 5 items
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('payments' in response.context)
        self.assertTrue(len(response.context['payments']) == 5)
    
    def test_view_with_no_transactions(self):
        """
        Test the view's behavior when there are no transactions for the client.
        """
        Transaction.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('payments' in response.context)
        self.assertEqual(len(response.context['payments']), 0)
    
    def test_invalid_client_returns_404(self):
        """
        Test that the view returns a 404 error for an invalid client ID.
        """
        url = reverse('sales:client_payment_history', args=[99999])  # Non-existent client ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_correct_client_in_context(self):
        """
        Test that the correct client object is passed in the context.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['client'], self.client_model)
    
    def test_transactions_ordered_by_date_descending(self):
        """
        Test that transactions are ordered by date in descending order.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        transactions = response.context['transactions']
        self.assertTrue(all(transactions[i].date >= transactions[i + 1].date for i in range(len(transactions) - 1)))


class DeleteTransactionViewTest(TestCase):
    """
    Test cases for the DeleteTransactionView.

    This class contains unit tests to verify the functionality and behavior of the DeleteTransactionView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test client and a transaction for deletion testing.
        """
        self.client_model = Client.objects.create(first_name="Juan", last_name="Perez")
        self.transaction = Transaction.objects.create(
            client=self.client_model,
            total_amount=100,
            method='cash'
        )
        self.url = reverse('sales:delete', args=[self.transaction.id])
    
    def test_delete_transaction_GET(self):
        """
        Test the GET request to the delete transaction page.

        Verifies that the page loads correctly and uses the correct template.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales/delete.html')
        self.assertIn('transaction', response.context)
    
    def test_delete_transaction_POST(self):
        """
        Test the POST request to delete a transaction.

        Ensures that the transaction is deleted and the user is redirected.
        """
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('sales:list_payment'))
        self.assertFalse(Transaction.objects.filter(id=self.transaction.id).exists())
    
    def test_delete_transaction_POST_success_message(self):
        """
        Test that a success message is displayed after deleting a transaction.
        """
        response = self.client.post(self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "La transacción ha sido eliminada correctamente.")
    
    def test_delete_transaction_404(self):
        """
        Test the response for a non-existent transaction.
        
        Ensures that a 404 error is returned when trying to delete a non-existent transaction.
        """
        url = reverse('sales:delete', args=[99999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_transaction_GET_shows_correct_transaction(self):
        """
        Test that the correct transaction is shown on the delete confirmation page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.context['transaction'], self.transaction)
    
    def test_delete_transaction_POST_actually_deletes(self):
        """
        Test that the POST request actually deletes the transaction from the database.
        """
        self.client.post(self.url)
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(id=self.transaction.id)


class ListPaymentViewTest(TestCase):
    """
    Test cases for the ListPaymentView.

    This class contains unit tests to verify the functionality and behavior of the ListPaymentView in the application.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.

        Creates test clients, services, appointments, and transactions for testing.
        """
        # Create clients
        cls.client1 = Client.objects.create(first_name="Juan", last_name="Perez")
        cls.client2 = Client.objects.create(first_name="Maria", last_name="Leon")
        
        # Create services
        cls.service1 = Service.objects.create(name="Express", price=20)
        cls.service2 = Service.objects.create(name="Facial", price=50)
        
        # Create appointments
        cls.appointment1 = Appointment.objects.create(client=cls.client1, date=timezone.now())
        cls.appointment1.services.add(cls.service1)
        cls.appointment2 = Appointment.objects.create(client=cls.client2, date=timezone.now() + timedelta(days=1))
        cls.appointment2.services.add(cls.service2)
        
        # Create transactions
        for i in range(35):  # Create 35 transactions for pagination testing
            Transaction.objects.create(
                client=cls.client1 if i % 2 == 0 else cls.client2,
                appointment=cls.appointment1 if i % 2 == 0 else cls.appointment2,
                total_amount=100,
                date=timezone.now() - timedelta(days=i)
            )
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Initializes the URL for the list payment view.
        """
        self.url = reverse('sales:list_payment')
    
    def test_view_url_exists_at_desired_location(self):
        """
        Test that the view is accessible at the expected URL.
        """
        response = self.client.get('/sales/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """
        Test that the view is accessible using its name in URL reversing.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """
        Test that the view uses the correct template for rendering.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales/list_payment.html')
    
    def test_pagination_is_thirty(self):
        """
        Test that pagination is working and displays 30 items per page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('list_transactions' in response.context)
        self.assertTrue(isinstance(response.context['list_transactions'], Page))
        self.assertEqual(len(response.context['list_transactions']), 30)
    
    def test_lists_all_transactions(self):
        """
        Test that all transactions are listed across multiple pages.
        """
        # Get second page and confirm it has (exactly) remaining 5 items
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('list_transactions' in response.context)
        self.assertEqual(len(response.context['list_transactions']), 5)
    
    def test_transactions_ordered_by_date_descending(self):
        """
        Test that transactions are ordered by date in descending order.
        """
        response = self.client.get(self.url)
        transactions = response.context['transactions']
        self.assertTrue(all(transactions[i].date >= transactions[i + 1].date for i in range(len(transactions) - 1)))
    
    def test_context_contains_client(self):
        """
        Test that the context contains a client object.
        """
        response = self.client.get(self.url)
        self.assertTrue('client' in response.context)
        self.assertIsInstance(response.context['client'], Client)
    
    def test_prefetch_related_data(self):
        """
        Test that related data is prefetched to minimize database queries.
        """
        response = self.client.get(self.url)
        transactions = response.context['transactions']
        with self.assertNumQueries(0):  # No additional queries should be made
            for transaction in transactions:
                transaction.client
                transaction.appointment
                list(transaction.appointment.services.all())
    
    def test_empty_transaction_list(self):
        """
        Test the view's behavior when there are no transactions.
        """
        Transaction.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('list_transactions' in response.context)
        self.assertEqual(len(response.context['list_transactions']), 0)
        self.assertFalse('client' in response.context)


class RegisterTransactionViewTest(TestCase):
    """
    Test cases for the RegisterTransactionView.

    This class contains unit tests to verify the functionality and behavior of the RegisterTransactionView in the
    application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test client, services, an appointment, and initializes the URL for testing.
        """
        self.client_model = Client.objects.create(first_name="Juan", last_name="Perez")
        self.service1 = Service.objects.create(name="Express", price=Decimal('20.00'))
        self.service2 = Service.objects.create(name="Facial", price=Decimal('50.00'))
        self.appointment = Appointment.objects.create(
            client=self.client_model,
            date=timezone.now().date(),
            start_time=timezone.now().time()
        )
        self.appointment.services.add(self.service1, self.service2)
        self.url = reverse('sales:register_transaction', args=[self.appointment.id])
    
    def test_view_url_exists_at_desired_location(self):
        """
        Test that the view is accessible at the expected URL.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """
        Test that the view uses the correct template for rendering.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'sales/register_transaction.html')
    
    def test_get_request_initial_form_data(self):
        """
        Test that the form is pre-populated with initial data when accessed via a GET request.

        Verifies that fields like `client`, `total_amount`, and `services` are initialized correctly.
        """
        response = self.client.get(self.url)
        self.assertIn('transaction_form', response.context)
        form = response.context['transaction_form']
        self.assertEqual(form.initial['client'], self.client_model.id)
        self.assertEqual(form.initial['total_amount'], Decimal('70.00'))
        self.assertQuerySetEqual(form.initial['services'], self.appointment.services.all(), ordered=False)
    
    def test_post_valid_data(self):
        """
        Test submitting valid data via a POST request.

        Ensures that a transaction is created successfully and redirects to the payment list page.
        """
        data = {
            'client': self.client_model.id,
            'services': [self.service1.id, self.service2.id],
            'method': 'cash',
            'total_amount': Decimal('70.00')
            
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('sales:list_payment'))
        transaction = Transaction.objects.first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.total_amount, Decimal('70.00'))
        self.assertEqual(transaction.client, self.client_model)
        self.assertQuerySetEqual(transaction.services.all(), [self.service1, self.service2], ordered=False)
    
    def test_post_invalid_data(self):
        """
        Test submitting invalid data via a POST request.

        Verifies that validation errors are displayed for invalid fields, such as an invalid payment method.
        """
        data = {
            'client': self.client_model.id,
            'services': [],
            'method': 'invalid_method',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['transaction_form']
        self.assertIn('method', form.errors)
        self.assertEqual(
            form.errors['method'][0],
            'Escoja una opción válida. invalid_method no es una de las opciones disponibles.'
        )
    
    def test_post_success_message(self):
        """
        Test that a success message is displayed after successfully registering a transaction.
        """
        data = {
            'client': self.client_model.id,
            'services': [self.service1.id, self.service2.id],
            'method': 'cash',
            'total_amount': Decimal('70.00')
        }
        response = self.client.post(self.url, data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Transacción registrada exitosamente.")
    
    def test_non_existent_appointment(self):
        """
        Test accessing the view with a non-existent appointment ID.

        Ensures that a 404 error is returned when trying to register a transaction for a non-existent appointment.
        """
        url = reverse('sales:register_transaction', args=[99999])  # Non-existent appointment ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_total_amount_calculation(self):
        """
        Test that the total amount is correctly calculated based on selected services.

        Ensures that only the prices of selected services are included in the total.
        """
        data = {
            'client': self.client_model.id,
            'services': [self.service1.id],  # Only one service
            'method': 'cash',
            'total_amount': Decimal('70.00')
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('sales:list_payment'))
        transaction = Transaction.objects.first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.total_amount, Decimal('20.00'))  # Price of service1
