"""For dynamic forms."""
from django import template
register = template.Library()


@register.filter(name='get_form')
def get_form(obj, index):
    """Get form index."""
    try:
        return obj[index]
    except:
        return None
