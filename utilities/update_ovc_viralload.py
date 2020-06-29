import json
import requests

from django.conf import settings
from django.db import connection

from cpovc_ovc.models import (OVCViralload)
from cpovc_ovc.functions import method_once


class UpdateViralLoad(object):
	"""Update ovc_viral_load"""
	def __init__(self):
		self.api_url_base = settings.NASCOP_API_BASE_URL
		self.login_url = settings.NASCOP_LOGIN_URL
		self.email = settings.NASCOP_EMAIL
		self.password = settings.NASCOP_PASSWORD
		self.numbers_to_facilities_list = self.query_ccc_numbers_to_facilities()
		# divide the data into 7 chunks.
		self.seven_chunks = self.chunk_it(self.numbers_to_facilities_list, 7)
	
	def query_ccc_numbers_to_facilities(self):
		with connection.cursor() as c:
			c.execute("SELECT ccc_number, facility_code, person_id FROM eid;")
			ccc_numbers_to_facilities = c.fetchall()
		return ccc_numbers_to_facilities
	
	def chunk_it(self, seq, num):
		# divide ccc_numbers-to-facilities list into manageable chunks so
		# requests don't time-out.

		avg = len(seq) / float(num)
		out = []
		last = 0.0
		
		while last < len(seq):
			out.append(seq[int(last):int(last + avg)])
			last += avg
			
		return out

	def generate_token(self):
		headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		credentials = { "email": self.email, "password": self.password }
		response = requests.post(self.login_url, headers=headers, data=credentials)
		
		if response.status_code == 200:
			json_token = json.loads(response.content)
			print(json.loads(response.content.decode('utf-8')))
			api_token = json_token.get('token')
			return api_token
		else:
			print(response)


	def get_viral_load(self, token, facility, patientID):
		headers = {'Authorization': 'Bearer {0}'.format(token)}
		api_url = '{0}{1}/{2}'.format(self.api_url_base, facility, patientID)
		response = requests.get(api_url, headers=headers)

		if response.status_code == 200:
			json_object = json.loads(response.content)
			data_list = []
			for test in json_object:
				patient = test.get('PatientID')
				date_tested = test.get('DateTested')
				result = test.get('Result')
				data = (patient, date_tested, result)
				data_list.append(data)
			return data_list
		elif response.status_code == 404:
			print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
			return None
		elif response.status_code == 401:
			print('[!] [{0}] Authentication Failed'.format(response.status_code), response.content)
			return None
		elif response.status_code == 400:
			print('[!] [{0}] Bad Request for PatientID: {1}'.format(response.status_code, patientID), response.content)
			return None
		elif response.status_code >= 300:
			print('[!] [{0}] Unexpected Redirect'.format(response.status_code), response.content)
			return None
		elif response.status_code >= 500:
			print('[!] [{0}] Server Error'.format(response.status_code), response.content)
			return None
		else:
			print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
			return None

	def vl_to_int(self, string):
		if not string:
			return int(-995)
		elif "< LDL" in string:
			return int(0)
		elif "nvalid" in string:
			return int(-998)
		elif "ailed" in string:
			return int(-999)
		elif "ollect" in string:
			return int(-997)
		elif not string.strip():
			return int(-996)
		else:
			return ''.join([i for i in string if i.isdigit()])

	def loop_through_data(self):
		chunks = self.seven_chunks
		try:
			for chunk in chunks:
				api_token = self.generate_token()

				for row in chunk:
					facility_code = row[1]
					ccc_number = row[0]
					person_id = row[2]
					facility_code_ccc = (facility_code, ccc_number)
					viral_load_records = self.get_viral_load(api_token, facility_code, ccc_number)
					if viral_load_records:
						for record in viral_load_records:
							date_tested = record[1]
							result = record[2]
							result_to_int = self.vl_to_int(result)
							# check if viral load is empty and update
							if OVCViralload.objects.filter(person_id=person_id, viral_date=date_tested, viral_load__isnull=True).exists():
								OVCViralload.objects.filter(person_id=person_id, viral_date=date_tested, viral_load__isnull=True).update(viral_load=result_to_int)
							# check if record exists before inserting
							elif OVCViralload.objects.filter(person_id=person_id, viral_date=date_tested).exists() == False:
								vl = OVCViralload(person_id=person_id, viral_load=result_to_int, viral_date=date_tested)
								vl.save()
								
		except Exception as e:
			print 'error exiting - %s' % (str(e))
			raise e
		else:
			pass

