
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

    def test_new_hivscreeningtool_get(self):
        event = mommy.make(OVCCareEvents, person=self.person)
        facility = mommy.make(OVCFacility, facility_name='Kenyatta')
        mommy.make(
            OVCHIVRiskScreening, event=event, facility=facility,
            person=self.person)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'forms/new_hivscreeningtool.html')

    def test_new_hivscreeningtool_post_invalid_choices(self):
        now = timezone.now()
        date_of_assessment = now - timedelta(days=300)
        facility = mommy.make(
            OVCFacility, facility_name='Kenyatta National Hospital')

        post_data = {
            'HIV_RA_1A': date_of_assessment,
            'HIV_RS_01': 'NO',
            'HIV_RS_02': 'ANNO',
            'HIV_RS_03': 'NO',
            'HIV_RS_03A': 'NO',
            'HIV_RS_04': 'NO',
            'HIV_RS_05': 'NO',
            'HIV_RS_06': 'NO',
            'HIV_RS_07': 'NO',
            'HIV_RS_08': 'NO',
            'HIV_RS_09': 'NO',
            'HIV_RS_10': 'NO',
            'HIV_RS_11': 'NO',
            'HIV_RS_14': 'NO',
            'HIV_RS_15': now - timedelta(days=100),
            'HIV_RS_16': 'NO',
            'HIV_RS_17': now - timedelta(days=90),
            'HIV_RS_18': 'NO',
            'HV_RS_18A': 'lorem ipsum',
            'HIV_RS_18B': '2',
            'HIV_RS_19': now - timedelta(days=80),
            'HIV_RS_21': 'NO',
            'HIV_RS_22': now - timedelta(days=70),
            'HIV_RS_23': 'ANNO',
            'HIV_RS_24': now - timedelta(days=60),
            'HIV_RA_3Q6': facility.id
        }
        person = mommy.make(RegPerson, surname='John')

        # create a house hold to attach the child
        house_hold = mommy.make(OVCHouseHold, head_person=person)

        # Add the OVC to a house hold
        mommy.make(OVCHHMembers, person=self.person, house_hold=house_hold)

        # Create an event
        mommy.make(OVCCareEvents, person=self.person)
        response = self.client.post(self.url, post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'forms/new_hivscreeningtool.html')
        self.assertContains(
            response,
            'Select a valid choice. NO is not one of the available choices'
        )

    def test_new_hivscreeningtool_post_valid_choices(self):
        now = timezone.now()
        date_of_assessment = now - timedelta(days=300)
        facility = mommy.make(
            OVCFacility, facility_name='Kenyatta National Hospital')

        post_data = {
            'HIV_RA_1A': date_of_assessment,
            'HIV_RS_01': 'ANNO',
            'HIV_RS_02': 'ANNO',
            'HIV_RS_03': 'ANNO',
            'HIV_RS_03A': 'ANNO',
            'HIV_RS_04': 'ANNO',
            'HIV_RS_05': 'ANNO',
            'HIV_RS_06': 'ANNO',
            'HIV_RS_07': 'ANNO',
            'HIV_RS_08': 'ANNO',
            'HIV_RS_09': 'ANNO',
            'HIV_RS_10': 'ANNO',
            'HIV_RS_11': 'ANNO',
            'HIV_RS_14': 'ANNO',
            'HIV_RS_15': now - timedelta(days=100),
            'HIV_RS_16': 'ANNO',
            'HIV_RS_17': now - timedelta(days=90),
            'HIV_RS_18': 'ANNO',
            'HV_RS_18A': 'lorem ipsum',
            'HIV_RS_18B': '2',
            'HIV_RS_19': now - timedelta(days=80),
            'HIV_RS_21': 'ANNO',
            'HIV_RS_22': now - timedelta(days=70),
            'HIV_RS_23': 'ANNO',
            'HIV_RS_24': now - timedelta(days=60),
            'HIV_RA_3Q6': facility.id
        }
        person = mommy.make(RegPerson, surname='John')

        # create a house hold to attach the child
        house_hold = mommy.make(OVCHouseHold, head_person=person)

        # Add the OVC to a house hold
        mommy.make(OVCHHMembers, person=self.person, house_hold=house_hold)

        # Create an event
        mommy.make(OVCCareEvents, person=self.person)
        response = self.client.post(self.url, post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'forms/new_hivscreeningtool.html')
        self.assertContains(response, 'lorem ipsum')
