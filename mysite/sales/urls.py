"""
URL Configuration for the Sales app.

This module defines the URL patterns for the Sales application.
It maps URLs to view functions, allowing users to interact with sales and payment-related features.

URL Patterns:
    - '': Maps to the list_payment view, displaying all payments.
    - 'client-payment-history/<int:client_id>/': Maps to the client_payment_history view, showing payment history for a
      specific client.
    - 'register-transaction/<int:appointment_id>/': Maps to the register_transaction view, for registering a transaction
      related to a specific appointment.

Note:
    The 'app_name' variable is set to 'sales', which is used for namespacing these URLs.

Usage:
    To include these URLs in the main project URLs, use:
    path('sales/', include ('sales.urls'))
"""
from django.urls import path

from . import views


app_name = 'sales'

urlpatterns = [
    path('', views.list_payment, name="list_payment"),
    path('client-payment-history/<int:client_id>/', views.client_payment_history, name="client_payment_history"),
    path('delete/<int:transaction_id>/', views.delete_transaction, name="delete"),
    path('register-transaction/<int:appointment_id>/', views.register_transaction, name="register_transaction"),
]