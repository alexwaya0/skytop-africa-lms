from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Custom filter to access dictionary items safely in templates.
    Usage: {{ my_dict|get_item:key }}
    """
    return dictionary.get(key)