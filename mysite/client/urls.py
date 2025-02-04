"""
URL routing configuration for the client management application.

This module defines the URL patterns for the application. Each pattern is associated with a specific view that will
handle requests to that URL. The views handle various functionalities related to client management, including
listing clients, importing clients, adding a new client, updating existing clients, deleting clients, and exporting
the client list to an Excel file.

Client URL Patterns:

    - '': The root URL of the application, which directs to the client view to display all clients.
    - 'import/': URL for uploading an Excel file containing client data.
    - 'add/': URL for adding a new client via a form.
    - 'edit/<int:client_id>/': URL for editing the information of a specific client identified by client_id.
    - 'delete/<int:client_id>/': URL for confirming and processing the deletion of a specific client identified
        by client_id.
    - 'export/': URL for exporting the list of clients to an Excel file.
    - 'search/': URL for searching for a client.
    - 'view/<int:client_id>/': URL for viewing full information about a client.

Voucher Client URL Patterns:

    - 'assign/<int:client_id>/': URL for assigning a voucher to a specific client.
    - 'client_details/<int:voucher_id>/': URL for viewing the details of a voucher assigned to a client.
    - 'client_delete/<int:voucher_id>/': URL for deleting a voucher associated with a client.
    - 'client_edit/<int:voucher_id>/': URL for editing the details of a voucher associated with a client.
    - 'client_list/<int:client_id>/': URL for listing all vouchers assigned to a specific client.

Each path is linked to a corresponding view function defined in the 'views' module.

Note:
    The 'app_name' variable is set to 'client', which is used for namespacing these URLs.
    
Usage:
    To include these URLs in the main project URLs, use:
    path('client/', include('client.urls'))
"""

from django.urls import path

from . import views


app_name = 'client'

urlpatterns = [
    # Path client:
    path('', views.list_client, name="client_list"),
    path('add/', views.add_client, name='client_add'),
    path('edit/<int:client_id>/', views.edit_client, name='client_edit'),
    path('delete/<int:client_id>/', views.delete_client, name='client_delete'),
    path('export/', views.export_clients, name='client_export'),
    path('import/', views.import_clients, name='client_import'),
    path('search/', views.search_client, name='client_search'),
    path('view/<int:client_id>/', views.view_detail_client, name='client_view'),
    
    # Path voucher client:
    path('assign/<int:client_id>/', views.assign_voucher, name='voucher_assign'),
    path('client_details/<int:voucher_id>/', views.voucher_client_details, name='voucher_client_details'),
    path('client_delete/<int:voucher_id>/', views.delete_client_voucher, name='voucher_client_delete'),
    path('client_edit/<int:voucher_id>/', views.edit_client_voucher, name='voucher_client_edit'),
    path('client_list/<int:client_id>/', views.voucher_list, name='voucher_client_list'),
    ]
    