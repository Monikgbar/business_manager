from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'client', 'total_amount', 'method']
    search_fields = ['client__first_name', 'client__last_name']
