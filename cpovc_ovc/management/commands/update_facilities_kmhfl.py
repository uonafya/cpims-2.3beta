from django.core.management.base import BaseCommand
from utilities.auto_update_facility_list import KMHFLFacilities

class Command(BaseCommand):
	help = 'Update KMHFL facilities'

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		KMHFLFacilities().get_newest_facilities()
		self.stdout.write('----- Updated KMHFL Facilities -----')
