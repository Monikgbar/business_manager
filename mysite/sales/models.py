from django.db import models


class Transaction(models.Model):
    """
    Represents a transaction in the system.

    This model stores information about transactions, including the associated appointment, client, services, date,
    total amount, and payment status.
    """
    PAYMENT_METHODS = [
        ('cash', 'Efectivo'),
        ('visa', 'Tarjeta'),
    ]
    appointment = models.ForeignKey('appointment.Appointment', verbose_name="cita", on_delete=models.CASCADE,
                                    null=True, blank=True)
    client = models.ForeignKey('client.Client', verbose_name="cliente", on_delete=models.CASCADE)
    services = models.ManyToManyField('service.Service', verbose_name="servicios", blank=True,
                                      related_name="transactions")
    date = models.DateTimeField(verbose_name="fecha", auto_now_add=True)
    total_amount = models.DecimalField(verbose_name="total servicios", max_digits=10, decimal_places=2, default=0)
    method = models.CharField(verbose_name="modo de pago", max_length=8, choices=PAYMENT_METHODS, default='visa')
    
    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['client'])
        ]
    
    def __str__(self):
        """
        Returns a string representation of the transaction.

        Returns:
            str: A string describing the transaction with client and date.
        """
        return f"Transacción de {self.client} - {self.date}"