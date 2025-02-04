from django.core.validators import RegexValidator
from django.db import models


class Employee(models.Model):
    """
    Model representing an employee in the system.

    This model stores basic information about an employee, including their first name, last name, telephone number,
    email address, services they are associated with, and a color preference for identification purposes.
    """
    first_name = models.CharField(verbose_name="nombre", max_length=50)
    last_name = models.CharField(verbose_name="apellido", max_length=100)
    telephone_number = models.CharField(
        verbose_name="nº de teléfono",
        unique=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}$',
                message="Ingrese un número de teléfono válido."
            )
        ]
    )
    email = models.EmailField(verbose_name="email", unique=True, null=True, blank=True)
    services = models.ManyToManyField(
        'service.Service',
        verbose_name="servicios realizados",
        related_name="employees",
        blank=True  # Allows employees without associated services
    )
    color = models.CharField(verbose_name="color", max_length=7, default='#3498db')
    
    class Meta:
        verbose_name = "empleado"
        ordering = ["first_name", "last_name"]
    
    def __str__(self):
        """
        String representation of the employee.

        :return: The full name of the employee (first name + last name).
        """
        return f"{self.first_name} {self.last_name}"
