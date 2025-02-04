from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    """
    Represents a category for services.

    This model stores information about service categories, including the name and color.
    """
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(verbose_name="color", max_length=7, default='#ffffff')
    
    class Meta:
        verbose_name = "categoría"
        ordering = ["name"]
        
    def __str__(self):
        """
        Returns a string representation of the category.

        Returns:
            str: The name of the category.
        """
        return self.name


class Service(models.Model):
    """
    Represents a service offered.

    This model stores information about services, including name, duration, price, category, and availability.
    """
    class Available(models.TextChoices):
        """
        Choices for service availability.
        """
        POSITIVE = 'SI', 'Sí',
        NEGATIVE = 'NO', 'No'
        
    name = models.CharField(verbose_name="nombre", max_length=100)
    duration = models.DurationField(verbose_name="duración", help_text="Duración del servicio", null=True, blank=True)
    price = models.DecimalField(verbose_name="precio", max_digits=6, decimal_places=2, default=0.00)
    category = models.ForeignKey(
        'Category',
        verbose_name="categoría",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="services")
    available = models.CharField(
        verbose_name='disponibiidad',
        max_length=2,
        choices=Available,
        default=Available.POSITIVE,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "servicio"
        ordering = ["name"]
    
    def __str__(self):
        """
        Returns a string representation of the service.

        Returns:
            str: The name of the service.
        """
        return f"{self.name}"
    
    @property
    def color(self):
        """
        Returns the color of the service's category, or white if no category is set.

        Returns:
            str: The color as a hex code.
        """
        return self.category.color if self.category else '#ffffff'
    

class Voucher(models.Model):
    """
    Represents a voucher for services.

    This model stores information about vouchers, including name, associated services, number of sessions, pricing, and
    discount information.
    """
    name = models.CharField(verbose_name="nombre del bono", max_length=250)
    services = models.ManyToManyField(Service, verbose_name="servicios", related_name="vouchers")
    total_sessions = models.PositiveIntegerField(verbose_name="número de sesiones")
    price_session = models.DecimalField(verbose_name="precio sesión", max_digits=8, decimal_places=2, default=0.00)
    discount = models.IntegerField(verbose_name="descuento (%)", help_text="Ingrese un valor entre 0 y 100",
                                   validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    discounted_price = models.DecimalField(verbose_name="precio con descuento", max_digits=8, decimal_places=2,
                                           editable=False, default=0.0)
    
    class Meta:
        verbose_name = 'bono'
        ordering = ['name']
    
    def __str__(self):
        """
        Returns a string representation of the voucher.

        Returns:
            str: The name of the voucher.
        """
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        """
        Overrides the default save method to calculate the discounted price before saving.
        """
        # Total price without discount
        total_price = self.price_session * self.total_sessions
        # Apply discount (convert discount to Decimal)
        discount_as_decimal = Decimal(self.discount) / 100
        self.discounted_price = Decimal(total_price) * (1 - discount_as_decimal)
        super().save(*args, **kwargs)
    
    def clean(self):
        """
        Validates the voucher data.

        Raises:
            ValidationError: If the discount is not between 0 and 100, or if the price is not greater than 0.
        """
        if not (0 <= self.discount <= 100):
            raise ValidationError(" El descuento debe estar entre 0 y 100.")
        if self.price_session <= 0:
            raise ValidationError("El precio debe ser mayor que 0.")
    
    
    
    
    


    