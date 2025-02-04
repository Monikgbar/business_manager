from datetime import timedelta, datetime, date

from django.db import models
from django.utils.timezone import now


class Appointment(models.Model):
    """
    Represents an appointment in the system.

    This model stores information about appointments, including the client, services, employee, date, time, and any
    additional notes.
    """
    client = models.ForeignKey(
        'client.Client',
        verbose_name='cliente',
        on_delete=models.CASCADE,
        related_name="clients"
    )
    services = models.ManyToManyField(
        'service.Service',
        verbose_name='servicio',
        related_name="appointments"
    )
    employee = models.ForeignKey(
        'employee.Employee',
        verbose_name='empleado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
       )
    date = models.DateField(verbose_name='fecha', default=now)
    start_time = models.TimeField(verbose_name='inicio', default='00:00')
    end_time = models.TimeField(verbose_name='fin', default='00:00', null=True, blank=True)
    notes = models.TextField(verbose_name='notas', null=True, blank=True)
    
    class Meta:
        verbose_name = "cita"
        ordering = ["start_time", "client"]
        indexes = [models.Index(fields=["start_time"])]
    
    def __str__(self):
        """
        Returns a string representation of the appointment.

        Returns:
            str: A string describing the appointment with client, date, and start time.
        """
        return f"Cita de {self.client} el {self.date} a las {self.start_time}"
    
    def title(self):
        """
        Generates a title for the appointment, including client name and services.

        Returns:
            str: A formatted string with the client's name and list of services.
        """
        service_names = "\n ".join(service.name for service in self.services.all())
        return f"{self.client.first_name} {self.client.last_name}\n{service_names}"
    
    def calculate_end_time(self):
        """
        Calculates the total duration of all services in the appointment.

        Returns:
            timedelta: The total duration of all services.
        """
        total_duration = sum((service.duration for service in self.services.all()), timedelta())
        # Convert time to datetime
        start_datetime = datetime.combine(date.today(), self.start_time)
        # Add the duration
        end_datetime = start_datetime + total_duration
        # Return only the time part
        return end_datetime

