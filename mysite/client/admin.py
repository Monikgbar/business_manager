from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    This class include information about how to display the model on the administration site and how to interact with
    it.
    """
    list_display = ['first_name', 'last_name', 'telephone_number']
    search_fields = ['first_name', 'last_name', 'telephone_number']
    ordering = ['first_name', 'last_name']
    
    
