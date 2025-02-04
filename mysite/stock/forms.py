from django import forms

from .models import Product, StockMovement


class ProductForm(forms.ModelForm):
    """
    A form for managing 'Product' objects.

    This form includes fields for product details such as name, supplier, description, price, and stock. Custom widgets
    are used to enhance the user interface.

    :param Meta: Specifies the model and fields to be used in the form, along with custom widgets.
    """
    class Meta:
        """
        Metaclass for ProductForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = Product
        fields = ['name', 'supplier', 'description', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'})
        }
        
    def __init__(self, *args, **kwargs):
        """
        Initialize the ProductForm.

        Sets an empty label for the supplier field.
        """
        super().__init__(*args, **kwargs)
        self.fields['supplier'].empty_label = "Selecciona un proveedor"
    
    
class StockMovementForm(forms.ModelForm):
    """
    A form for managing 'StockMovement' objects.
    
    This form includes fields for stock movement details such as quantity, movement type, and reason. Custom widgets are
    used to enhance the user interface.
    
    :param Meta: Specifies the model and fields to be used in the form, along with custom widgets.
    """
    
    class Meta:
        """
        Metaclass for StockMovementForm.

        Defines the model, fields to include, and widgets for form rendering.
        """
        model = StockMovement
        fields = ['quantity', 'movement_type', 'reason']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'})
        }
        
        def clean_quantity(self):
            """
            Clean and validate the quantity field.

            This method checks if a quantity value has been provided and raises a ValidationError if it's missing.

            :return: The cleaned quantity value.
            :rtype: int or float
            :raises ValidationError: If the quantity is None or not provided.
            """
            quantity = self.cleaned_data.get('quantity')
            if quantity is None:
                raise forms.ValidationError('La cantidad es requerida')
            return quantity
        