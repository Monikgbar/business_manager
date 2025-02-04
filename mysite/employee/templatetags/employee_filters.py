from django import template


register = template.Library()


@register.filter
def startswith(value, arg):
    """
    Check if the value starts with the specified argument.

    This is a custom template filter that checks if a string (value) starts with another string (arg).

    Args:
        value (str): The string to check.
        arg (str): The substring to look for at the beginning of 'value'.

    Returns:
        bool: True if 'value' starts with 'arg', False otherwise.

    Example:
        In a template, you can use it like this:
        {% if some_string|startswith:"prefix" %}
            This string starts with "prefix"
        {% endif %}
    """
    return value.startswith(arg)
