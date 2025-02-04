"""
URL Configuration for the Appointment app.

This module defines the URL patterns for the Appointment application.
It maps URLs to view functions, allowing users to interact with appointment-related features.

URL Patterns:
    - '': Maps to the calendar view, displaying the agenda.
    - 'create/': Maps to the appointment creation view.
    - 'detail/<int:appointment_id>/': Maps to the appointment detail view.
    - 'delete/<int:appointment_id>/': Maps to the appointment deletion view.

Note:
    The 'app_name' variable is set to 'appointment', which is used for namespacing these URLs.

Usage:
    To include these URLs in the main project URLs, use:
    path('appointment/', include('appointment.urls'))
"""

from django.urls import path

from . import views


app_name = 'appointment'

urlpatterns = [
    path('', views.calendar_view, name="agenda"),
    path('create/', views.appointment_create, name="create"),
    path('detail/<int:appointment_id>/', views.appointment_detail, name="detail"),
    path('delete/<int:appointment_id>/', views.appointment_delete, name="delete"),
]
