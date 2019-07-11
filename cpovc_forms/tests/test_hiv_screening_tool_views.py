
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from cpovc_registry.models import RegPerson
from cpovc_forms.models import OVCCareEvents, OVCHIVRiskScreening
from cpovc_ovc.models import OVCFacility, OVCHHMembers, OVCHouseHold

user_model = get_user_model()


class TestHivScreenToolViews(TestCase):
    def setUp(self, *args, **kwargs):
        self.person = mommy.make(RegPerson, surname='John')
        self.url = reverse(
            'new_hivscreeningtool', kwargs={'id': self.person.id})
        person_2 = mommy.make(RegPerson, surname='test')
        user = mommy.make(
            user_model, username='test_user', reg_person=person_2)
        user.set_password('test_user')
        user.save()
        self.client.login(username='test_user', password='test_user')
        super(TestHivScreenToolViews, self).setUp(*args, **kwargs)

    def test_new_hivscreeningtool_get(self):
        event = mommy.make(
            OVCCareEvents, person=self.person, event_type_id='HRST')
        facility = mommy.make(
            OVCFacility, facility_name='Kenyatta', facility_code=12000)
        mommy.make(
            OVCHIVRiskScreening, event=event,
            facility_code=facility.facility_code,
            person=self.person)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'forms/new_hivscreeningtool.html')
