import json
import requests

from django.conf import settings

from cpovc_ovc.models import (OVCFacility)
from cpovc_ovc.functions import method_once



class KMHFLFacilities(object):
    '''
        Auto-update the list of facilities from KMHFL
    '''

    def __init__(self):
        self.username = settings.KMHFL_USERNAME
        self.password = settings.KMHFL_PASSWORD
        self.scope = settings.KMHFL_SCOPE
        self.grant_type = settings.KMHFL_GRANT_TYPE
        self.client_id = settings.KMHFL_CLIENTID
        self.client_secret = settings.KMHFL_CLIENT_SECRET
        self.api_base_url = settings.KMHFL_API_BASE_URL
        self.facility_base_url = settings.KMHFL_FACILITY_BASE_URL
        self.sub_county_base_url = settings.KMHFL_SUBCOUNTY_BASE_URL
        self.login_url = settings.KMHFL_LOGIN_URL
        self.api_token = self.generate_token()
        self.latest_facility = self.latest_facility()

    @method_once
    def latest_facility(self):
        # query latest facility from db
        latest_mfl_code = OVCFacility.objects.values("facility_code").exclude(facility_code__regex=r'[^0-9]').order_by('facility_code').last()
        if latest_mfl_code is not None:
            return latest_mfl_code["facility_code"]
        else:
            return 0

    @method_once
    def generate_token(self):
        # generate token.
        login_url = self.login_url
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth = (self.client_id, self.client_secret)
        credentials = { "grant_type": self.grant_type, 
                        "username": self.username, 
                        "password": self.password, 
                        "scope": self.scope }
        response = requests.post(login_url, headers=headers, data=credentials, auth=auth)
        if response.status_code == 200:
            json_token = json.loads(response.content)
            api_token = json_token.get('access_token')
            return api_token
        else:
            print(response.content)
    

    def get_facilities(self):
        # request for facilities
        headers = {'Authorization': 'Bearer {0}'.format(self.api_token)}
        api_url = '{0}facilities/facilities/'.format(self.api_base_url)
        params = {'fields':'id,code,official_name,sub_county_id,subcounty_name', 
                  'format':'json', 'page_size':'50'}
        response = requests.get(api_url, headers=headers, params=params)
        
        if response.status_code == 200:
            json_object = json.loads(response.content)
            return json_object
        else:
            print(response.content, api_url)


    def get_subcounty_code(self, sub_county_id):
        # request facility and get sub-county id.
        headers = {'Authorization': 'Bearer {0}'.format(self.api_token)}
        params = {'format': 'json', 'fields':'code,name,county_name'}
        api_url = '{0}{1}'.format(self.sub_county_base_url, sub_county_id)
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            json_object = json.loads(response.content)
            cpims_subcounty_id = json_object["code"]
            return cpims_subcounty_id
        else:
            print(response, api_url)

    def get_newest_facilities(self):
        # loop for new facilities.
        try:
            data = self.get_facilities()
            results = data["results"]
            for facility in results:
                facility_code = facility["code"]
                if facility_code > self.latest_facility:
                    # facility_id = facility["id"]
                    sub_county_id = facility["sub_county_id"]
                    cpims_subcounty_id = self.get_subcounty_code(sub_county_id)
                    facility_name = facility["official_name"]
                    new_facility = OVCFacility(facility_code=facility_code, 
                        facility_name=facility_name, 
                        sub_county_id=cpims_subcounty_id)
                    
                    new_facility.save()
        
        except Exception as e:
            raise e
        else:
            pass


KMHFLFacilities().get_newest_facilities()