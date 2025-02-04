from django import forms

from .models import Appointment


class CreateAppointmentForm(forms.ModelForm):
    """
    A form for creating and managing 'Appointment' objects.

    This form includes fields for appointment details such as client, services, employee, date, start time, end time,
    and notes. Custom widgets are used to enhance the user interface, including the use of select2 for dropdown fields.

    :param Meta: Specifies the model and fields to be used in the form, along with custom widgets.
    """
    
    class Meta:
        """
        Metaclass for CreateAppointmentForm.

        Defines the model, fields to exclude, and widgets for form rendering.
        """
        model = Appointment
        exclude = ['created_at', 'updated_at']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control select2'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'employee': forms.Select(attrs={'class': 'form-control select2'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }
            
    def save(self, commit=True):
        """
        Save the form and create an Appointment instance.

        This method overrides the default save method to handle the many-to-many relationship with services.

        :param commit: Boolean indicating whether to save the instance to the database.
        :return: The saved Appointment instance.
        """
        appointment = super().save(commit=False)
        services = self.cleaned_data.get('services')
        if commit:
            appointment.save()
            appointment.services.set(services)
        return appointment