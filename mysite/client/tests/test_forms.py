from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.timezone import now

from client.forms import ClientForm, ClientVoucherForm, UploadExcelForm
from client.models import Client
from service.models import Voucher


class UploadExcelFormTest(TestCase):
    """
    Test case for the UploadExcelForm.

    This class contains tests to verify the functionality of the UploadExcelForm, including validation of various file
    types and error handling.
    """
    
    def test_valid_xlsx_file(self):
        """
        Test that the form is valid when a valid `.xlsx` file is uploaded.

        Steps:
        1. Upload a valid `.xlsx` file.
        2. Assert that the form is valid.
        """
        xlsx_file = SimpleUploadedFile(
            "tests.xlsx",
            b"some excel data",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        form_xlsx = UploadExcelForm(data={}, files={"excel_file": xlsx_file})
        self.assertTrue(form_xlsx.is_valid())
        
    def test_valid_xls_file(self):
        """
        Test that the form is valid when a valid `.xls` file is uploaded.

        Steps:
        1.  Upload a valid `.xls` file.
        2.  Assert that the form is valid.
        """
        xls_file = SimpleUploadedFile(
            "tests.xls",
            b"some excel data",
            content_type="application/vnd.ms-excel"
        )
        form_xls = UploadExcelForm(data={}, files={"excel_file": xls_file})
        self.assertTrue(form_xls.is_valid())

    def test_invalid_file_type(self):
        """
        Test that the form is invalid when a non-Excel file (e.g., `.txt`) is uploaded.

        Steps:
        1. Upload a `.txt` file.
        2. Assert that the form is invalid and contains the error "Formato de archivo no válido. Por favor, sube un
        archivo Excel.".
        """
        file_obj = SimpleUploadedFile("tests.txt", b"This is not an excel file", content_type="tests/plain")
        form = UploadExcelForm(data={}, files={"excel_file": file_obj})
        self.assertFalse(form.is_valid())
        self.assertIn("Formato de archivo no válido. Por favor, sube un archivo Excel.", form.errors["excel_file"])

    def test_empty_file(self):
        """
        Test that the form is invalid when no file is uploaded.

        Steps:
        1. Leave the file field empty.
        2. Assert that the form is invalid and contains the error "Este campo es obligatorio.".
        """
        form = UploadExcelForm(data={"excel_file": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("Este campo es obligatorio.", form.errors["excel_file"])


class ClientFormTest(TestCase):
    """
    Test case for the ClientForm.

    This class contains tests to verify the functionality of the ClientForm, including validation of form fields and
    error handling.
    """
    
    def test_valid_form(self):
        """
        Test that the form is valid when all required fields are correctly filled.

        Steps:
        1. Create a dictionary with valid client data.
        2. Instantiate the ClientForm with the data.
        3. Assert that the form is valid.
        """
        data = {
            "first_name": "Maria",
            "last_name": "Leon",
            "telephone_number": "621458963",
            "email": "marialeon@example.com"
        }
        form = ClientForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_name(self):
        """
        Test that the form is invalid when the first name is empty.

        Steps:
        1. Create a dictionary with client data, leaving the first name empty.
        2. Instantiate the ClientForm with the data.
        3. Assert that the form is invalid and contains the error "Este campo es obligatorio." for the first name field.
        """
        data = {"first_name": "", "last_name": "Leon", "email": "marialeon@example.com", "telephone_number": "621458963"}
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Este campo es obligatorio.", form.errors["first_name"])

    def test_invalid_email(self):
        """
        Test that the form is invalid when an incorrect email format is provided.

        Steps:
        1. Create a dictionary with client data, including an invalid email.
        2. Instantiate the ClientForm with the data.
        3. Assert that the form is invalid and contains the error "Introduzca una dirección de correo electrónico
        válida." for the email field.
        """
        data = {"first_name": "Maria", "last_name": "Leon", "email": "invalid_email", "telephone_number": "621458963"}
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Introduzca una dirección de correo electrónico válida.", form.errors["email"])


class ClientVoucherFormTest(TestCase):
    """
    Test case for the ClientVoucherForm.

    This class contains tests to verify the functionality of the ClientVoucherForm, including validation of form
    fields and error handling.
    """
    
    def setUp(self):
        """
        Set up the test environment.

        This method creates a Client and a Voucher object to be used in the tests.
        """
        self.client = Client.objects.create(first_name="Maria", last_name="Leon", email="marialeon@example.com")
        self.voucher = Voucher.objects.create(total_sessions=10)

    def test_valid_form(self):
        """
        Test that the form is valid when all required fields are correctly filled.

        Steps:
        1. Create a dictionary with valid client voucher data.
        2. Instantiate the ClientVoucherForm with the data.
        3. Assert that the form is valid.
        """
        data = {
            "client": self.client.id,
            "voucher": self.voucher.id,
            "purchase_date": now(),
            "expiration_date": now() + timedelta(days=90),
            "sessions_remaining": 10
        }
        form = ClientVoucherForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_client(self):
        """
        Test that the form is invalid when a non-existent client ID is provided.

        Steps:
        1. Create a dictionary with client voucher data, including a non-existent client ID.
        2. Instantiate the ClientVoucherForm with the data.
        3. Assert that the form is invalid and contains the error "Escoja una opción válida. Esa opción no está entre
        las disponibles." for the client field.
        """
        data = {
            "client": 0,  # Non-existent client ID
            "voucher": self.voucher.id,
            "purchase_date": now(),
            "expiration_date": now() + timedelta(days=90),
            "sessions_remaining": 10
        }
        form = ClientVoucherForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Escoja una opción válida. Esa opción no está entre las disponibles.", form.errors["client"])

    def test_invalid_voucher(self):
        """
        Test that the form is invalid when the voucher field is left empty.

        Steps:
        1. Create a dictionary with client voucher data, omitting the voucher field.
        2. Instantiate the ClientVoucherForm with the data.
        3. Assert that the form is invalid and contains the error "Este campo es obligatorio." for the voucher field.
        """
        data = {
            "client": self.client.id,
            "purchase_date": now(),
            "expiration_date": now() + timedelta(days=90),
        }
        form = ClientVoucherForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Este campo es obligatorio.", form.errors["voucher"])