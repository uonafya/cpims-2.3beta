from django import template

register = template.Library()

@register
def format_choice_fields(value):
    """Convert the choice fields into human readable formats"""
    options = {
        'SLSE': 'Secondary School',
        'SLPR': 'Primary School',
        'SLNS': 'No School',
        'HSTR': 'HSTR',
        'HSKN': 'HSKN',
        'HSTP': 'Positive',
        'XXXX': 'XXXX',
        'HSTN': 'Negative',
        'HSRT': 'HSRT',
        'ART': 'ART',
        'ARAR': 'ARAR',
        'ARV': 'ARV',
        'True': 'Yes',
        'False': 'No',
        'NULL': '-'
        'None': '-'
    }
    return options.get(value, None) or value