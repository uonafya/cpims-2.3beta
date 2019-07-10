from django.test import TestCase
from model_mommy import mommy

from cpovc_main.models import SchoolList, SetupGeography 


class TestSchoolListModel(TestCase):
    """Tests for the SchoolList model """
    def test_school_creation(self):
        ward = mommy.make(
            SetupGeography, 
            area_name='Makongeni', area_code='GWRD'
        )
        sub_county = mommy.make(
            SetupGeography, 
            area_name='Makongeni Sub County', area_code='GDIS'
        )
        data = {
            'school_name': 'Kenyatta High School',
            'type_of_school': 'SLSE',
            'school_ward': ward,
            'school_subcounty': sub_county
        }
        school = mommy.make(SchoolList, **data)
        self.assertEqual(1, SchoolList.objects.count())
        self.assertEqual(data.get('school_name'), school.school_name)
        self.assertEqual(
            data.get('type_of_school'), school.type_of_school)
        self.assertEqual('Makongeni', school.school_ward.area_name)
        self.assertEqual(
            'Makongeni Sub County', school.school_subcounty.area_name)
