from django import forms

from .models import Employee


# Color input field
class ColorInput(forms.widgets.Input):
    """
    A custom form widget that renders an input field of type 'color'.

    This widget allows the user to select a color from a color picker.
    It is used for fields where the user needs to choose a color, such as employee-specific color preferences.

    :param input_type:
        The input type is set to 'color', enabling the color picker in HTML forms.
    """
    input_type = "color"
    
    
class EmployeeForm(forms.ModelForm):
    """
    A form for adding or editing employee details.

    This form allows the creation and modification of employee information, including their first name, last name,
    telephone number, email, and color preference.

    :param Meta:
        Specifies the model and fields to be used in the form. It also configures widgets to customize the appearance
        of the form fields, such as adding placeholder text and applying specific CSS classes.

    :return:
        A ModelForm based on the Employee model that handles employee data input.
    """
    class Meta:
        """
        Metaclass for EmployeeForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = Employee
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            "telephone_number": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            "color": ColorInput(attrs={'class': 'form-control'})
        }
        
        
class ServicesEmployeeForm(forms.ModelForm):
    """
    A form for assigning services to employees.

    This form allows selecting which services are available for a specific employee by displaying a list of services as
    checkboxes.

    :param Meta:
        Specifies the model and fields to be used in the form. The 'services' field is rendered as a set of checkboxes,
        allowing the selection of multiple services.

    :return:
        A ModelForm based on the Employee model that handles the assignment of services to an employee.
    """
    class Meta:
        """
        Metaclass for ServicesEmployeeForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = Employee
        fields = ['services']
        widgets = {'services': forms.CheckboxSelectMultiple, }
        
