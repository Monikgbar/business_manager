from django import forms
from django.core.exceptions import ValidationError

from .models import Client, ClientVoucher
from service.models import Voucher


class UploadExcelForm(forms.Form):
    """
   Form for uploading Excel files.

   This form validates the uploaded file to ensure it is in Excel format (either .xlsx or .xls).
   """
    excel_file = forms.FileField()
    
    def clean_excel_file(self):
        """
        Validate the uploaded Excel file.

        Ensures that the uploaded file has a valid Excel extension (.xlsx or .xls).

        :raises forms.ValidationError: If the file is not an Excel file.
        :return: The uploaded Excel file.
        """
        excel_file = self.cleaned_data["excel_file"]
        file_name = excel_file.name.lower()
        if not (file_name.endswith(".xlsx") or file_name.endswith(".xls")):
            raise forms.ValidationError("Formato de archivo no válido. Por favor, sube un archivo Excel.")
        return excel_file


class ClientForm(forms.ModelForm):
    """
    Form for creating and updating Client instances.

    This form includes custom validation to check for duplicate emails and telephone numbers for clients.
    """
    class Meta:
        """
        Metaclass for ClientForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = Client
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "telephone_number": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'})
        }
        
    def clean_email(self):
        """
        Validate the email field.

        Checks if the provided email already exists in the database for another client.

        :raises forms.ValidationError: If the email is already in use.
        :return: The validated email address.
        """
        email = self.cleaned_data.get('email')
        if email:
            if Client.objects.filter(email=email).exists():
                raise forms.ValidationError(f"Ya existe un usuario con el email {email}.")
        return email
    
    def clean_telephone_number(self):
        """
        Validate the telephone number field.

        Checks if the provided telephone number already exists in the database for another client.

        :raises forms.ValidationError: If the telephone number is already in use.
        :return: The validated telephone number.
        """
        telephone_number = self.cleaned_data.get('telephone_number')
        if telephone_number:
            if Client.objects.filter(telephone_number=telephone_number).exists():
                raise forms.ValidationError(f"Ya existe un usuario con el número {telephone_number}.")
        return telephone_number


class ClientVoucherForm(forms.ModelForm):
    """
    Form for associating a Client with a Voucher.

    This form allows selecting a client and a voucher, along with setting the purchase date, expiration date, and the
    number of remaining sessions.
    """
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        empty_label=None
    )
    voucher = forms.ModelChoiceField(
        queryset=Voucher.objects.all(),
        empty_label="Selecciona un bono",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    class Meta:
        """
        Metaclass for ClientVoucherForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = ClientVoucher
        fields = ['client', 'voucher', 'purchase_date', 'expiration_date']
        widgets = {
            "purchase_date": forms.DateInput(attrs={'class': 'form-control'}),
            "expiration_date": forms.DateInput(attrs={'class': 'form-control'}),
            "sessions_remaining": forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        """
        Validate purchase and expiration dates.

        This method checks that the expiration date is after the purchase date.

        :return: Cleaned form data
        :raises ValidationError: If expiration date is not after purchase date
        """
        cleaned_data = super().clean()
        purchase_date = cleaned_data.get('purchase_date')
        expiration_date = cleaned_data.get('expiration_date')
    
        if purchase_date and expiration_date and expiration_date <= purchase_date:
            raise ValidationError('La fecha de expiración debe ser posterior a la fecha de compra.')
        return cleaned_data
