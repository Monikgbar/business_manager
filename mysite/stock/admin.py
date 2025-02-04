from django.contrib import admin

from .models import Product, Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    This class include information about how to display the model on the administration site and how to interact with
    it.
    """
    list_display = ['name']
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    This class include information about how to display the model on the administration site and how to interact with
    it.
    """
    list_display = ['supplier', 'name', 'price', 'stock']
    search_fields = ['name', 'supplier']
    ordering = ['supplier', 'name']

    