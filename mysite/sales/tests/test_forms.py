from decimal import Decimal

from django import forms
from django.test import TestCase
from django.utils import timezone

from sales.forms import TransactionForm
from client.models import Client
from service.models import Service
from appointment.models import Appointment


class TransactionFormTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(first_name="Juan", last_name="Perez")
        self.service = Service.objects.create(name="Express", price=Decimal('20.00'))
        self.appointment = Appointment.objects.create(
            client=self.client,
            date=timezone.now().date(),
            start_time=timezone.now().time()
        )

    def test_transaction_form_valid_data(self):
        form_data = {
            'appointment': self.appointment.id,
            'client': self.client.id,
            'services': [self.service.id],
            'total_amount': Decimal('20.00'),
            'method': 'cash'
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_transaction_form_invalid_data(self):
        form_data = {
            'appointment': '',
            'client': '',
            'services': [],
            'total_amount': '',
            'method': ''
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # client, total_amount, and method are required

    def test_transaction_form_excluded_fields(self):
        form = TransactionForm()
        self.assertNotIn('date', form.fields)

    def test_transaction_form_widgets(self):
        form = TransactionForm()
        self.assertIsInstance(form.fields['appointment'].widget, forms.Select)
        self.assertIsInstance(form.fields['client'].widget, forms.HiddenInput)
        self.assertIsInstance(form.fields['services'].widget, forms.CheckboxSelectMultiple)
        self.assertIsInstance(form.fields['total_amount'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['method'].widget, forms.Select)

    def test_transaction_form_widget_attributes(self):
        form = TransactionForm()
        self.assertEqual(form.fields['appointment'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['total_amount'].widget.attrs['readonly'], 'readonly')
        self.assertEqual(form.fields['method'].widget.attrs['class'], 'form-control')

    def test_transaction_form_services_widget(self):
        form = TransactionForm()
        self.assertEqual(form.fields['services'].widget.attrs['class'], 'form-check-input')

    def test_transaction_form_total_amount_readonly(self):
        form_data = {
            'appointment': self.appointment.id,
            'client': self.client.id,
            'services': [self.service.id],
            'total_amount': Decimal('30.00'),  # Different from service price
            'method': 'cash'
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())
        # The form should accept the provided total_amount even if it's different from the service price
        # because the field is readonly in the widget. The actual validation/calculation should be done in the view.
        self.assertEqual(form.cleaned_data['total_amount'], Decimal('30.00'))