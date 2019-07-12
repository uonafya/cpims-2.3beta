from unittest import TestCase

from data_cleanup.templatetags import format_choice_fields


class TestFormatChoiceFields(TestCase):
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
        'None': '-'
    }
    def test_filtering_option_tags_value_recognized(self):
        for key, value in self.options:
            self.assertEqual(format_choice_fields(key), value)

    def test_filter_choice_field_value_not_recognized(self):
        self.assertEqual(
            'SOME_VALUE',
            format_choice_fields('SOME_VALUE')
        )