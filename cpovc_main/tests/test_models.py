from django.test import TestCase
from model_mommy import mommy
from cpovc_main.models import FacilityList
from cpovc_main.models import SchoolList, SetupGeography 
from cpovc_main.models import SetupGeography 
from cpovc_main.models import SetupList 
from cpovc_main.models import Forms


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


class FacilityListModel(TestCase):
    """Tests for the facility_list model """
    def test_facility_creation(self):
        data = {
            'facility_code' : 12,
            'facility_name' : 'healthit',
            'county_id' : '1',
            'county_name' : 'uontowers',
            'subcounty_id' : 12,
            'subcounty_name' : '12th',
            'latitude' : 1233.00,
            'longitude' : 123.09
        }
        facility = mommy.make(FacilityList, **data)
        self.assertEqual(1, FacilityList.objects.count())
        self.assertEqual(data.get('facility_code'), facility.facility_code)
        self.assertEqual(data.get('facility_name'), facility.facility_name)
        self.assertEqual(data.get('county_id'), facility.county_id)
        self.assertEqual(data.get('county_name'), facility.county_name)
        self.assertEqual( data.get('subcounty_id'), facility.subcounty_id)
        self.assertEqual( data.get('subcounty_name'), facility.subcounty_name)
        self.assertEqual( data.get('latitude'), facility.latitude)
        self.assertEqual( data.get('longitude'), facility.longitude)


class TestSetupGeography(TestCase):
    """Tests for the Setup_Geography model """
    def test_setup_geography(self):
        data = {
            'area_type_id' : 123,
            'area_name' : 'healthit',
            'area_code' : 'GDIS',
            'parent_area_id' : 1233,
            'area_name_abbr' : 'UNES'
        }      
        
        setupgeo = mommy.make(SetupGeography, **data)    # let create the recored on setupgeo model
        self.assertEqual(1, SetupGeography.objects.count())   # count created to  be one
        self.assertEqual(data.get('area_type_id'), setupgeo.area_type_id)
        self.assertEqual(data.get('area_name'), setupgeo.area_name)
        self.assertEqual(data.get('area_code'), setupgeo.area_code)
        self.assertEqual(data.get('parent_area_id'), setupgeo.parent_area_id)
        self.assertEqual( data.get('area_name_abbr'), setupgeo.area_name_abbr)


class Testsetuplist(TestCase):
    """Tests for the setuplist model """
    def test_setup_list(self):
        data = {
            'item_id' : 12,
            'item_description' : 'FSM', 
            'item_description_short' : 'female sex workets', 
            'item_category' : 'sex workers', 
            'item_sub_category' : 'sex worker', 
            'the_order' : 123, 
            'user_configurable' : True, 
            'sms_keyword' : False
        }
        testsetuplist = mommy.make(SetupList, **data)    # let create the recored on setupgeo model
        self.assertEqual(1, SetupList.objects.count())   # count created to  be one
        self.assertEqual(data.get('item_id'), testsetuplist.item_id )
        self.assertEqual(data.get('item_description'), testsetuplist.item_description )
        self.assertEqual(data.get('item_description_short'), testsetuplist.item_description_short)
        self.assertEqual(data.get('item_category'), testsetuplist.item_category)
        self.assertEqual( data.get('item_sub_category'), testsetuplist.item_sub_category)
        self.assertEqual(data.get('the_order'), testsetuplist.the_order)
        self.assertEqual(data.get('user_configurable'), testsetuplist.user_configurable)
        self.assertEqual(data.get('sms_keyword'), testsetuplist.sms_keyword)


class testforms(TestCase):
    """Tests for the setuplist model """
    def Test_forms(self):
        data = {
            'form_guid' : 'healthyit',
            'form_title' : 'sicking',
            'form_type_id' : '12',
            'form_subject_id' : 89,
            'form_area_id' : 67,
            'person_id_filled_paper' : 17,
            'org_unit_id_filled_paper' : 122,
            'capture_site_id' : 1223,
            'user_id_created' : 'uontroes'
        }
        testformsmodel = mommy.make(Forms, **data)    # let create the recored on setupgeo model
        self.assertEqual(1, Forms.objects.count())   # count created to  be one for the model itself
        self.assertEqual(data.get('form_guid'), testformsmodel.form_guid )
        self.assertEqual(data.get('form_title'), testformsmodel.form_title )
        self.assertEqual(data.get('form_type_id'), testformsmodel.form_type_id)
        self.assertEqual(data.get('form_subject_id'), testformsmodel.form_subject_id)
        self.assertEqual( data.get('form_area_id'), testformsmodel.form_area_id)
        self.assertEqual(data.get('person_id_filled_paper'), testformsmodel.person_id_filled_paper)
        self.assertEqual(data.get('org_unit_id_filled_paper'), testformsmodel.org_unit_id_filled_paper)
        self.assertEqual(data.get('capture_site_id'), testformsmodel.capture_site_id)
        self.assertEqual(data.get('user_id_created'), testformsmodel.user_id_created)
      
            
