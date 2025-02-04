from datetime import timedelta
from django import template


register = template.Library()


@register.filter
def format_duration(value):
    """
    Format a timedelta object into a string representation of hours and minutes.

    Args:
        value (timedelta): The duration to format.

    Returns:
        str: A string in the format "HH:MM" representing the duration.
             Returns "Valor no válido" if the input is not a timedelta object.

    Usage in template:
        {{ my_duration|format_duration }}
    """
    if not isinstance(value, timedelta):
        return "Valor no válido"
  
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}"
   

