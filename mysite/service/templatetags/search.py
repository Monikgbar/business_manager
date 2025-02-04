from django import template


register = template.Library()


@register.filter
def instanceof(obj, class_name):
    """
    Check if an object is an instance of a specified class.

    This filter compares the lowercase name of the object's class with the provided class name (case-insensitive).

    Args:
        obj: The object to check.
        class_name (str): The name of the class to compare against.

    Returns:
        bool: True if the object is an instance of the specified class, False otherwise.

    Usage in template:
        {% if my_object|instanceof:"MyClass" %}
            This object is an instance of MyClass
        {% endif %}
    """
    return obj.__class__.__name__.lower() == class_name.lower()
