from django import template

register = template.Library()


@register.filter(name='gen_value')
def gen_value(value, args):
    if value in args:
        return args[value]
    else:
        return value
