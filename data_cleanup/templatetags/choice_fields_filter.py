from django import template

register = template.Library()


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
        'NULL': '-',
         None: '-',
        'None': '-',
        'SMAL': 'Male',
        'SFEM': 'Female',
        True: 'Yes',
        False: 'No',
    }
    return options.get(value, None) or value

register.filter('format_choice_fields', format_choice_fields)