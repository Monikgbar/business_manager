from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import EmployeeForm, ServicesEmployeeForm
from .models import Employee
from service.models import Category, Service


def add_employee(request):
    """
    Add a new employee to the database.
    
    This view handles the POST request to add a new employee using a form. If the form is valid, it saves the
    new employee to the database and redirects to the employee list page.
    
    :param request: HttpRequest object containing request details.
    
    :return:
        - Redirects to the 'employee' page if the employee is added successfully.
        - Renders the 'add.html' template with the form if no POST request or form is invalid.
    """
    form = EmployeeForm()
    services_categories = Category.objects.prefetch_related('services').all()
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        
        if form.is_valid():
            employee = form.save(commit=False)
            selected_services = request.POST.getlist('services')
            employee.save()
            employee.services.set(selected_services)
            return redirect(reverse('employee:view', args=[employee.id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        
    return render(request, 'employee/add.html', {
        'form': form,
        'services_categories': services_categories,
    })


def assign_services(request, employee_id):
    """
    Assign services to an employee.

    This view allows an administrator to assign available services to an employee. Services are grouped by category
    and displayed in a form. Upon form submission, the selected services are assigned to the employee.

    :param request: HttpRequest object containing request details.

    :param employee_id: Integer ID of the employee to whom services will be assigned.

    :return:
        - Redirects to the 'employee:services' page after successfully assigning services.
        - Renders the 'assign_services.html' template with the services form if no POST request or form is invalid.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Group services by category.
    services = (Service.objects.filter(available=Service.Available.POSITIVE).select_related('category')
                .order_by('category__name'))
    # Create the form with the available services
    form = ServicesEmployeeForm(initial={'services': services})
    
    if request.method == 'POST':
        form = ServicesEmployeeForm(request.POST)
        if form.is_valid():
            selected_services = form.cleaned_data['services']
            employee.services.set(selected_services)
            return redirect(reverse('employee:services', args=[employee_id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
    return render(
        request,
        'employee/assign_services.html',
        {
            'form': form,
            'employee': employee,
            'services': services,
        }
    )


def edit_employee(request, employee_id):
    """
    Edit an existing employee's details.
    
    This view allows updating the information of an employee with a specific ID. If a POST request with valid data is
    provided, it updates the employee's information in the database.
    
    :param request: HttpRequest object containing request details.
    
    :param employee_id: Integer ID of the employee to be edited.
    
    :return:
        - Redirects to the 'employee' page if the update is successful.
        - Renders the 'client_edit.html' template with the employee's current data if no POST request.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse('employee:list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = EmployeeForm(instance=employee)
    
    return render(
        request,
        'employee/edit.html',
        {'form': form, 'employee': employee}
    )


def delete_employee(request, employee_id):
    """
    Delete an employee from the database.
    
    This view displays a confirmation page for deleting an employee with a specific ID. If confirmed via a POST request,
    the employee is deleted from the database and the user is redirected to the employee list page.
    
    :param request: HttpRequest object containing request details.
    
    :param employee_id: Integer ID of the employee to be deleted.
    
    :return:
        - Redirects to the 'employee:list' page after successful deletion.
        - Renders the 'delete.html' template to confirm deletion if no POST request.
    """
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        employee.delete()
        
        return redirect(reverse('employee:list'))
    
    return render(request, 'employee/delete.html', {'employee': employee})


def list_employee(request):
    """
    Display a list of all employees, ordered by their first names.

    Retrieves all employees from the database, orders them by first name, and renders them on the 'list.html' template.

    :param request: HttpRequest object containing request details.

    :return: HttpResponse containing the rendered 'list.html' template with the list of employees.
    """
    
    employees = Employee.objects.all().order_by('first_name')
    
    return render(request, 'employee/list.html', {'employees': employees})


def services_employee(request, employee_id):
    """
    Display the services assigned to an employee.

    This view retrieves an employee's assigned services and groups them by their categories. The services are then
    displayed on the 'services.html' template.

    :param request: HttpRequest object containing request details.

    :param employee_id: Integer ID of the employee whose services are to be displayed.

    :return: HttpResponse containing the rendered 'services.html' template with the employee's services.
    """
    employee = Employee.objects.prefetch_related(
        Prefetch('services', queryset=Service.objects.order_by('category'))
    ).get(id=employee_id)
    services = employee.services.all()
    
    return render(request, 'employee/services.html', {'employee': employee, 'services': services})

    
def view_details_employee(request, employee_id):
    """
    Display detailed information of a specific employee.

    This view retrieves an employee with a specific ID and renders their details on the 'view.html' template.

    :param request: HttpRequest object containing request details.
    
    :param employee_id: Integer ID of the employee whose details are to be viewed.
    
    :return: HttpResponse containing the rendered 'view.html' template with employee details.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    
    return render(request, 'employee/view.html', {'employee': employee})

