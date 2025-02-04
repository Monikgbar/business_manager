from django.core.exceptions import ValidationError
from django.db import models


class Supplier(models.Model):
    """
    Represents a supplier of products.

    This model stores information about suppliers, including their name.
    """
    name = models.CharField(verbose_name="nombre", max_length=250)
    
    class Meta:
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"
        ordering = ["name"]
        
    def __str__(self):
        """
        Returns a string representation of the supplier.

        Returns:
            str: The name of the supplier.
        """
        return self.name


class Product(models.Model):
    """
    Represents a product in the inventory.

    This model stores information about products, including name, description, supplier, price, stock, and last update
    time.
    """
    name = models.CharField(verbose_name="nombre", max_length=250)
    description = models.TextField(verbose_name="descripción", blank=True, null=True)
    supplier = models.ForeignKey(
        Supplier,
        verbose_name="proveedor",
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True)
    price = models.DecimalField(verbose_name="precio", max_digits=10, decimal_places=2, default=0.0)
    stock = models.PositiveIntegerField(verbose_name="stock", default=0)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "producto"
        ordering = ["name"]
    
    def __str__(self):
        """
        Returns a string representation of the product.

        Returns:
            str: The name of the product.
        """
        return self.name
    
    def clean(self):
        """
        Validate price field.

        This method ensures the price is not a negative value.

        :raises ValidationError: If price is negative
        """
        if self.price < 0:
            raise ValidationError({'El precio no puede ser un valor negativo.'})
        
    def save(self, *args, **kwargs):
        """
        Save the model instance with validation.

        Performs full validation before saving to ensure data integrity.

        :return: The saved model instance
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    def reduce_stock(self, quantity):
        """
        Reduces the stock of the product by the specified quantity.

        Args:
            quantity (int): The quantity to reduce from the stock.

        Raises:
            ValueError: If there is insufficient stock.
        """
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        else:
            raise ValueError("Stock insuficiente")


class StockMovement(models.Model):
    """
    Represents a movement in the stock of a product.
    
    This model stores information about stock movements, including the product, quantity, type of movement, reason, and
    creation time.
    """
    MOVEMENT_CHOICES = [
        ('increase', 'Aumento'),
        ('decrease', 'Reducción'),
    ]
    
    REASON_CHOICES = [
        ('cabin_expense', 'Gasto en cabina'),
        ('sale', 'Venta'),
        ('disrepair', 'Mal estado'),
        ('increase stock', 'Aumento de stock'),
    ]
    
    product = models.ForeignKey(
        Product,
        verbose_name="producto",
        on_delete=models.CASCADE,
        related_name='stock_movement')
    quantity = models.IntegerField(verbose_name="cantidad")
    movement_type = models.CharField(verbose_name="tipo de movimiento", max_length=8, choices=MOVEMENT_CHOICES,
                                     blank=True, null=True)
    reason = models.CharField(verbose_name="motivo de gasto", max_length=16, choices=REASON_CHOICES)
    created_at = models.DateTimeField(verbose_name="fecha de registro", auto_now_add=True)
    
    def __str__(self):
        """
        Returns a string representation of the stock movement.

        Returns:
            str: A string describing the product, movement type, and quantity.
        """
        return f"{self.product.name} - {self.movement_type} ({self.quantity})"
    
