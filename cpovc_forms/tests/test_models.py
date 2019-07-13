from django.test import TestCase
from model_mommy import mommy

from cpovc_forms.models import OVCMonitoring, OVCHouseHold, OVCCareEvents


class TestOVCMonitoringModel(TestCase):
    """Tests for the OVCMonitoring model """
    def test_cpmonitoring_creation(self):
        event = mommy.make(
            OVCCareEvents,
            event_type_id='FSAM'
        )
        household = mommy.make(
            OVCHouseHold,
            head_identifier='20070940', head_person_id='3143465'
        )

        data = {
            'hiv_status_knowledge': 'Yes',
            'viral_suppression': 'Yes',
            'hiv_prevention': 'Yes',
            'undernourished': 'No',
            'access_money': 'Yes',
            'violence': 'Yes',
            'caregiver': 'No',
            'school_attendance': 'Yes',
            'school_progression': 'No',
            'cp_achievement': 'Yes',
            'case_closure': 'Yes',
            'case_closure_checked': 2,
            'quarter': 3,
            'event_date': '2019-04-02',
            'event_id': event,
            'household_id': household
        }
        cpmonitoring = mommy.make(OVCMonitoring, **data)
        self.assertEqual(1, OVCMonitoring.objects.count())
        self.assertEqual(data.get('hiv_status_knowledge'), cpmonitoring.hiv_status_knowledge)
        self.assertEqual(data.get('school_attendance'), cpmonitoring.school_attendance)
        self.assertEqual(data.get('caregiver'), cpmonitoring.caregiver)
        self.assertEqual(
            data.get('case_closure'), cpmonitoring.case_closure)
        self.assertEqual('event_date', cpmonitoring.event_date)
        self.assertEqual(
            'FSAM', cpmonitoring.event_id.event_type_id)
