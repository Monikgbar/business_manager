from django.contrib import admin

from .models import Category, Service, Voucher


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    This class include information about how to display the model on the administration site and how to interact with
    it.
    """
    list_display = ['name', 'category', 'price', 'duration']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    This class include information about how to display the model on the administration site and how to interact with
    it.
    """
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    """
    This class include information about how to display the model on the administration site and how to interact with
    it.
    """
    list_display = ['name', 'total_sessions', 'discounted_price']
    search_fields = ['name']
    ordering = ['name']
