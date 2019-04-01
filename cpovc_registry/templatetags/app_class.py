from django import template

register = template.Library()


@register.filter(name='get_class')
def get_class(value, args):
    if value == args:
        return 'active'
    else:
        split_vals = value.split('/')
        if split_vals[1] == args:
            return 'active'
        else:
            return ''
