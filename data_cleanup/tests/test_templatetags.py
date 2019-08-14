from datetime import datetime
from unittest import TestCase

from data_cleanup.templatetags.choice_fields_filter import format_choice_fields


class TestFormatChoiceFields(TestCase):
    options = {
        'SLSE': 'Secondary School',
        'SLPR': 'Primary School',
        'SLNS': 'No School',
        'HSTR': 'HSTR',
        'HSKN': 'HSKN',
        'HSTP': 'Positive',
        'XXXX': '-',
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
        for key, value in self.options.items():
            self.assertEqual(format_choice_fields(key), value)

    def test_filter_choice_field_value_not_recognized(self):
        self.assertEqual(
            'SOME_VALUE',
            format_choice_fields('SOME_VALUE')
        )

    def test_filtering_datetime_with_date_objects(self):
        """Checks that datetime objects are returned as is"""
        date_object = datetime.now()
        format_date_object_result = format_choice_fields(date_object)
        self.assertEqual(date_object, format_date_object_result)
