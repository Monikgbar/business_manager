import json
from itertools import groupby

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.dateparse import parse_datetime

from .forms import CreateAppointmentForm
from .models import Appointment
from employee.models import Employee
from client.models import Client
from service.models import Category, Service


def appointment_create(request):
    """
    Create a new appointment.

    This view handles both GET and POST requests for creating a new appointment.
    It prepares the necessary data for the appointment creation form and processes the form submission.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the appointment creation form or redirect to the agenda.

    :raises Http404: If the employee with the given ID does not exist.
    """
    clients = Client.objects.all()
    employees = Employee.objects.all()
    
    employee_id = request.GET.get('employee_id')  # Get the employee ID from URL
    if employee_id and employee_id.isdigit():
        employee = Employee.objects.filter(id=employee_id).first()
    else:
        messages.error(request, "Para empezar a añadir citas debes crear un empleado.")
        return redirect('appointment:agenda')
    
    # Filter services by the selected employee
    services = (employee.services.select_related('category')
                if employee else Service.objects.select_related('category')).order_by('category__name', 'name')
        
    services_by_category = [
        {'category': category, 'services': list(items)}
        for category, items in groupby(services, lambda s: s.category)
    ]
    
    # Durations of services
    service_durations = {service.name: service.duration.total_seconds() // 60 for service in services}
    
    initial_data = {}
    date_time_str = request.GET.get('date')
    if date_time_str:
        date_time = parse_datetime(date_time_str)
        if date_time:
            initial_data['date'] = date_time.date()
            initial_data['start_time'] = date_time.time()
    if employee:
        initial_data['employee'] = employee.id
            
    if request.method == 'POST':
        form = CreateAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            form.save_m2m()
            
            # Calculate end time
            if appointment.services.exists():
                appointment.end_time = appointment.calculate_end_time().time()
                appointment.save()
            
            return redirect(reverse('appointment:agenda'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CreateAppointmentForm(initial=initial_data)
   
    return render(request, 'appointment/create.html', {
        'form': form,
        'clients': clients,
        'employees': employees,
        'employee_id': employee_id,
        'services_by_category': services_by_category,
        'service_durations': json.dumps(service_durations),
    })

    
def appointment_detail(request, appointment_id):
    """
    Display and edit details of a specific appointment.

    This view handles both GET and POST requests for viewing and editing an appointment.
    It retrieves the appointment details and prepares the form for editing.

    :param request: The HTTP request object.
    :param appointment_id: The ID of the appointment to be viewed or edited.
    :return: Rendered HTML page with the appointment details and edit form.

    :raises Http404: If the appointment with the given ID does not exist.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    clients = Client.objects.all()
    employees = Employee.objects.select_related('employee')
    services = Service.objects.select_related('category').all().order_by('category__name', 'name')
    services_by_category = [
        {'category': category, 'services': list(items)}
        for category, items in groupby(services, lambda s: s.category)
    ]
    
    if request.method == 'POST':
        form = CreateAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect(reverse('appointment:agenda'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
    else:
        form = CreateAppointmentForm(instance=appointment)
        
    return render(request, 'appointment/detail.html', {
        'appointment': appointment,
        'form': form,
        'clients': clients,
        'employees': employees,
        'services_by_category': services_by_category,
    })


def appointment_delete(request, appointment_id):
    """
    Delete a specific appointment.

    This view handles the deletion of an appointment. It requires a POST request to actually delete the appointment.

    :param request: The HTTP request object.
    :param appointment_id: The ID of the appointment to be deleted.
    :return: Redirect to the agenda page after successful deletion, or confirmation page for GET requests.

    :raises Http404: If the appointment with the given ID does not exist.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment:agenda')
        
    return render(request, 'appointment/delete.html', {'appointment': appointment})


def calendar_view(request):
    """
    Display the calendar view with all appointments.

    This view prepares the data for the calendar display, including appointments for all employees. It formats the data
    for use with FullCalendar.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the calendar view.
    """
    appointments = Appointment.objects.all()
    employees = Employee.objects.all()
    appointment_data = []
    num_employees = employees.count()
    # Percentage for each column
    column_width = 100 / num_employees if num_employees > 0 else 100
    service_names = "Sin tratamiento"
    category_colors = ""  # Don't assign color if there aren't services
    
    if not employees.exists():
        # Handling the case of not having employees
        appointment_data = [{
            'employee_id': '',
            'employee_name': 'Sin empleados',
            'appointments': []
        }]
        column_width = 100
    else:
        for employee in employees:
            # Filter appointments for the current employee.
            employee_appointments = appointments.filter(employee=employee)
            employee_appointments_data = []
        
            # Generate appointment data only if it exists for the employee.
            for appointment in employee_appointments:
                if appointment.date and appointment.start_time and appointment.end_time:
                    # Generate data in ISO format for FullCalendar
                    start = f"{appointment.date}T{appointment.start_time}"
                    end = f"{appointment.date}T{appointment.end_time}"

                    # Check if the appointment has associated services
                    if appointment.services.exists():
                        service_names = appointment.title()
                        category_colors = ", ".join(
                            set(category.color for category in appointment.services.all() if category)
                        )
            
                    employee_appointments_data.append({
                        'id': appointment.id,
                        'title': appointment.title(),
                        'start': start,
                        'end': end,
                        'extendedProps': {
                            'client': f"{appointment.client.first_name} {appointment.client.last_name}",
                            'services': service_names,
                            'employee': f"{appointment.employee.first_name} {appointment.employee.last_name}",
                            'employee_id': appointment.employee.id,
                            'notes': appointment.notes or '',
                            'employeeColor': getattr(appointment.employee, 'color', ''),
                            'categoryColor': category_colors,
                        }
                    })
                    
            # Add the employee's details, including an empty list of appointments if they don't have any.
            appointment_data.append({
                'employee_id': employee.id,
                'employee_name': f"{employee.first_name} {employee.last_name}",
                'appointments': employee_appointments_data
            })

    return render(request, 'appointment/agenda.html', {
        'appointments_data': json.dumps(appointment_data, ensure_ascii=False),
        'column_width': column_width,
        'employees': employees
    })



    

