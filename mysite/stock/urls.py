"""
URL Configuration for the Stock Management app.

This module defines the URL patterns for the Stock Management application.
It maps URLs to view functions, allowing users to interact with suppliers, products, and stock movements.

URL Patterns:
    Supplier Views:
    - 'supplier/list/': Maps to the list_supplier view for listing all suppliers.
    - 'supplier/add/': Maps to the add_supplier view for creating a new supplier.
    - 'supplier/edit/<int:supplier_id>/': Maps to the edit_supplier view for editing an existing supplier.
    - 'supplier/delete/<int:supplier_id>/': Maps to the delete_supplier view for deleting a supplier.

    Product Views:
    - 'product/add/': Maps to the add_products view for creating a new product.
    - 'product/details/<int:product_id>/': Maps to the details_product view for viewing product details.
    - 'product/delete/<int:product_id>/': Maps to the delete_product view for deleting a product.
    - 'product/edit/<int:product_id>/': Maps to the edit_product view for editing an existing product.
    - 'product/products_supplier/<int:supplier_id>/': Maps to the products_supplier view for listing products of a
    specific supplier.
    - 'product/products/no-supplier/': Maps to the products_without_supplier view for listing products without a
    supplier.
    - 'product/search/': Maps to the search_product view for searching products.

    Stock Views:
    - 'stock/create_movement/<int:product_id>/': Maps to the create_stock_movement view for creating a stock movement
    for a specific product.

Note:
    The 'app_name' variable is set to 'stock', which is used for namespacing these URLs.

Usage:
    To include these URLs in the main project URLs, use:
    path('stock/', include('stock.urls'))
"""
from django.urls import path

from . import views


app_name = 'stock'

urlpatterns = [
    # Path for supplier views:
    path('supplier/list/', views.list_supplier, name="supplier_list"),
    path('supplier/add/', views.add_supplier, name="supplier_add"),
    path('supplier/edit/<int:supplier_id>/', views.edit_supplier, name="supplier_edit"),
    path('supplier/delete/<int:supplier_id>/', views.delete_supplier, name="supplier_delete"),
    
    # Path for product views:
    path('product/add/', views.add_products, name="product_add"),
    path('product/details/<int:product_id>/', views.details_product, name="product_details"),
    path('product/delete/<int:product_id>/', views.delete_product, name="product_delete"),
    path('product/edit/<int:product_id>/', views.edit_product, name="product_edit"),
    path('product/products_supplier/<int:supplier_id>/', views.products_supplier, name="product_products_supplier"),
    path('product/products/no-supplier/', views.products_without_supplier, name="product_products_without_supplier"),
    path('product/search/', views.search_product, name="product_search"),
    
    # Path for stock views
    path('stock/create_movement/<int:product_id>/', views.create_stock_movement, name="stock_create_movement")
]