from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Service, Voucher


class ColorInput(forms.widgets.Input):
    """
    A custom form widget that renders an input field of type 'color'.

    This widget allows the user to select a color from a color picker.
    It is used for fields where the user needs to choose a color, such as service-specific color preferences.

    :param input_type:
        The input type is set to 'color', enabling the color picker in HTML forms.
    """
    input_type = "color"
    

class ServiceForm(forms.ModelForm):
    """
    A form for managing 'Service' objects, including fields for name, category, price, duration, and availability.
    Custom widgets are used for enhanced user experience, and a custom `clean_duration` method validates the 'duration'
    field.
    
    :param Meta:
        Specifies the model and fields to be used in the form. It also configures widgets to customize the appearance
        of the form fields, such as adding placeholder text and applying specific CSS classes.

    :return:
        A ModelForm based on the Service model that handles service data input.
    """
    class Meta:
        """
        Metaclass for ServiceForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = Service
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM'}),
            'available': forms.Select(attrs={'class': 'form-control'})
        }
        
    def __init__(self, *args, **kwargs):
        """
        Initialize the ServiceForm.

        Sets an empty label for the category field.
        """
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Selecciona una categoría"
        
    def clean_duration(self):
        """
        Clean and validate the duration field.

        Converts the duration input to a timedelta object.

        :raises ValidationError: If the duration format is invalid.
        :return: A timedelta object representing the service duration.
        """
        duration = self.cleaned_data['duration']
        if isinstance(duration, str):
            hours, minutes = map(int, duration.split(":"))
            return timedelta(hours=hours, minutes=minutes)
        elif isinstance(duration, timedelta):
            return duration
        else:
            raise ValidationError("Formato de duración no válido.")
        
        
class CategoryForm(forms.ModelForm):
    """
    A form for managing 'Category' objects.

    This form includes fields for the category name and color.

    :param Meta: Specifies the model and fields to be used in the form, along with custom widgets.
    """
    class Meta:
        """
        Metaclass for CategoryForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = Category
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'color': ColorInput(attrs={'class': 'form-control'})
        }


class VoucherForm(forms.ModelForm):
    """
    A form for managing 'Voucher' objects.

    This form includes fields for voucher details such as name, services, price per session, total sessions, discount,
    and discounted price.

    :param Meta: Specifies the model and fields to be used in the form, along with custom widgets.
    """
    class Meta:
        """
        Metaclass for VoucherForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = Voucher
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'price_session': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_sessions': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control'})
        }
    
    