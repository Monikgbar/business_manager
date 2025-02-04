from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):
    """
    Form for creating or updating a Transaction.

    This form is based on the Transaction model and includes fields for appointment, client, total services, and payment
    status.
    """
    class Meta:
        """
        Metaclass for TransactionForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = Transaction
        exclude = ['date']
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.HiddenInput(),
            'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'method': forms.Select(attrs={'class': 'form-control'}),
        }