"""
URL routing configuration for the employee management application.

This module defines the URL patterns for the application. Each pattern is associated with a specific view that will
handle requests to that URL. The views handle various functionalities related to employee management, including
listing employee, adding a new employee, editing existing employee and deleting employees.

URL Patterns:

    - '': The root URL of the application, which directs to the employee view to display all employees.
    - 'add/': URL for adding a new employee via a form.
    - 'assign_services/': URL for assigning services to an employee.
    - 'edit/<int:employee_id>/': URL for editing the information of a specific employee identified by
        employee_id.
    - 'delete/<int:employee_id>/': URL for confirming and processing the deletion of a specific employee
        identified by employee_id.
    - 'services/<int:pk>/': URL for viewing the list of services assigned to each employee.
    - 'view/<int:employee_id>/': URL for viewing full information about an employee.

Each path is linked to a corresponding view function defined in the 'views' module.

Note:
    The 'app_name' variable is set to 'employee', which is used for namespacing these URLs.

Usage:
    To include these URLs in the main project URLs, use:
    path('employee/', include('employee.urls'))
"""

from django.urls import path

from . import views


app_name = 'employee'

urlpatterns = [
    path('', views.list_employee, name="list"),
    path('add/', views.add_employee, name="add"),
    path('assign_services/<int:employee_id>/', views.assign_services, name="assign_services"),
    path('edit/<int:employee_id>/', views.edit_employee, name="edit"),
    path('delete/<int:employee_id>/', views.delete_employee, name="delete"),
    path('services/<int:employee_id>/', views.services_employee, name="services"),
    path('view/<int:employee_id>/', views.view_details_employee, name="view"),
]