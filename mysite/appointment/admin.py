from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    This class include information about how to display the model on the administration site and how to interact with
    it.
    """
    list_display = ['client', 'start_time']
    search_fields = ['client__first_name', 'client__telephone_number']
    ordering = ['client', 'start_time']
