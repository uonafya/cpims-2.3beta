from django.test import TestCase
from model_mommy import mommy

from cpovc_main.models import SchoolList


class TestSchoolListModel(TestCase):
    """Tests for the SchoolList model """
    def test_school_creation(self):
        mommy.make(SchoolList, _quantity=5)
        self.assertEqual(5, SchoolList.objects.count())
    