from datetime import date, timedelta

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Client(models.Model):
    """
    Model representing a client.

    This model stores basic information about a client, including their first name,last name, telephone number,
    and email address. It also enforces uniqueness for the telephone number and email.
    """
    first_name = models.CharField(verbose_name="nombre", max_length=50)
    last_name = models.CharField(verbose_name="apellido", max_length=100)
    telephone_number = models.CharField(
        verbose_name="nº de teléfono",
        unique=True,
        null=True,
        blank=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{9,15}$',
                message="Ingrese un número de teléfono válido. Debe contener entre 9 y 15 dígitos."
            )
        ]
    )
    email = models.EmailField(verbose_name="email", unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "cliente"
        ordering = ["first_name", "last_name"]
    
    def __str__(self):
        """
        String representation of the client.

        :return: The full name of the client (first name + last name).
        """
        return f"{self.first_name} {self.last_name}"
    
    
def default_expiration_date():
    """
    Default function to set the expiration date.

    This function returns a date that is 90 days from the current date, which will be used as the default expiration
    date for client vouchers.

    :return: A date 90 days from today.
    """
    return date.today() + timedelta(days=90)

    
class ClientVoucher(models.Model):
    """
    Model representing a voucher associated with a client.

    This model stores the details of a client's voucher, including the associated client, voucher, purchase date,
    expiration date, the number of remaining sessions, and whether the voucher is active. It also provides methods to
    track and manage the remaining sessions.
    """
    VALID_CHOICES = [
        (True, 'Sí'),
        (False, 'No'),
    ]
    client = models.ForeignKey(Client, verbose_name="cliente", on_delete=models.CASCADE, related_name="vouchers")
    voucher = models.ForeignKey('service.Voucher', on_delete=models.CASCADE, related_name="client_voucher")
    purchase_date = models.DateField(verbose_name="fecha de compra", default=timezone.now)
    expiration_date = models.DateField(verbose_name="fecha de caducidad", default=default_expiration_date)
    sessions_remaining = models.PositiveIntegerField(verbose_name="sesiones restantes")
    is_active = models.BooleanField(verbose_name="estado", choices=VALID_CHOICES, default=True)
    
    class Meta:
        verbose_name = "bono del cliente"
        ordering = ["voucher", "purchase_date"]
        
    def __str__(self):
        """
        String representation of the client voucher.

        :return: The full name of the client, the voucher name and the remaining sessions.
        """
        return f"{self.client} - {self.voucher} ({self.sessions_remaining} sesiones restantes)."
    
    def save(self, *args, **kwargs):
        """
        Override the save method to initialize remaining sessions only for new instances.

        :param args: Additional arguments passed to the save method.
        :param kwargs: Additional keyword arguments passed to the save method.
        """
        if not self.pk and self.sessions_remaining is None:
            self.sessions_remaining = self.voucher.total_sessions
        super().save(*args, **kwargs)
        
    
    