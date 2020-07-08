from django.core.management.base import BaseCommand
from utilities.update_ovc_viralload import UpdateViralLoad

class Command(BaseCommand):
	help = 'Updates viral load for each existing and non-existing \
			OVCs'

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		UpdateViralLoad().loop_through_data()
		self.stdout.write('----- Updated viral loads -----')
