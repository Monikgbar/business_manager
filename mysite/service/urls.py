"""
URL routing configuration for the service management application.

This module defines the URL patterns for the Service Management application.
It maps URLs to view functions, allowing users to interact with services, categories, and vouchers.

URL Patterns:
    Service Views:
    - 'service/add/': Maps to the add_service view for creating a new service.
    - 'service/edit/<int:service_id>/': Maps to the edit_service view for editing an existing service.
    - 'service/delete/<int:service_id>/': Maps to the delete_service view for deleting a service.
    - 'service/services/category/<int:category_id>/': Maps to the services_category view for listing services in a
    category.
    - 'service/services/no-category/': Maps to the services_without_category view for listing services without a
    category.
    - 'service/view/<int:service_id>/': Maps to the view_details_service view for viewing service details.

    Category Views:
    - 'category/list/': Maps to the list_category view for listing all categories.
    - 'category/add/': Maps to the add_category view for creating a new category.
    - 'category/edit/<int:category_id>/': Maps to the edit_category view for editing an existing category.
    - 'category/delete/<int:category_id>/': Maps to the delete_category view for deleting a category.

    Voucher Views:
    - 'voucher/add/': Maps to the add_voucher view for creating a new voucher.
    - 'voucher/delete/<int:voucher_id>': Maps to the delete_voucher view for deleting a voucher.
    - 'voucher/details/<int:voucher_id>': Maps to the details_voucher view for viewing voucher details.
    - 'voucher/edit/<int:voucher_id>': Maps to the edit_voucher view for editing an existing voucher.
    - 'voucher/list/': Maps to the voucher_list view for listing all vouchers.

    Shared Views:
    - 'shared/items/search/<str:model_name>': Maps to the search_items view for searching items across different models.

Note:
    The 'app_name' variable is set to 'service', which is used for namespacing these URLs.

Usage:
    To include these URLs in the main project URLs, use:
    path('services/', include('service.urls'))
"""

from django.urls import path

from . import views


app_name = 'service'

urlpatterns = [
    # Path for service views:
    path('service/add/', views.add_service, name="service_add"),
    path('service/edit/<int:service_id>/', views.edit_service, name="service_edit"),
    path('service/delete/<int:service_id>/', views.delete_service, name="service_delete"),
    path('service/services/category/<int:category_id>/', views.services_category, name="service_services_category"),
    path('service/services/no-category/', views.services_without_category, name="service_services_without_category"),
    path('service/view/<int:service_id>/', views.view_details_service, name="service_view"),
    
    # Path for category views:
    path('category/list/', views.list_category, name="category_list"),
    path('category/add/', views.add_category, name="category_add"),
    path('category/edit/<int:category_id>/', views.edit_category, name='category_edit'),
    path('category/delete/<int:category_id>/', views.delete_category, name="category_delete"),
    
    # Path for voucher views:
    path('voucher/add/', views.add_voucher, name="voucher_add"),
    path('voucher/delete/<int:voucher_id>', views.delete_voucher, name="voucher_delete"),
    path('voucher/details/<int:voucher_id>', views.details_voucher, name="voucher_details"),
    path('voucher/edit/<int:voucher_id>', views.edit_voucher, name="voucher_edit"),
    path('voucher/list/', views.voucher_list, name="voucher_list"),
    
    # Path for shared views:
    path('shared/items/search/<str:model_name>', views.search_items, name="service_search_items"),
]
