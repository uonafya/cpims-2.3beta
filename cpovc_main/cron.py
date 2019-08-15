import logging
from crontab import CronTab

import settings

"""
Task Scheduler
==============
This module manages periodic tasks using cron.
"""

class CronManager(object):

	def __init__(self):
		self.cron = CronTab(user=True)

	def add_hourly(self, name, user, command, environment=None):
		# Add an hourly cron task
		cron_job = self.cron.new(command=command, user=user)
		cron_job.minute.on(0)
		cron_job.hour.during(0,23)
		cron_job.enable()
		self.cron.write()
		if self.cron.render():
			print self.cron.render()
			return True

	def add_daily(self, name, user, command, environment=None):
		# Add a daily cron task
		cron_job = self.cron.new(command=command, user=user)
		cron_job.minute.on(0)
		cron_job.hour.on(0)
		cron_job.enable()
		self.cron.write()
		if self.cron.render():
			print self.cron.render()
			return True

	def add_weekly(self, name, user, hour, day, command, environment=None):
		# Add a weekly cron task, the parameters hour, day should be integers.
		cron_job = self.cron.new(command=command)
		cron_job.minute.on(0)
		cron_job.hour.on(hour)
		cron_job.dow.on(day)
		cron_job.enable()
		self.cron.write()
		if self.cron.render():
			print self.cron.render()
			return True

	def add_monthly(self, name, user, command, environment=None):
		# Add a monthly cron task
		cron_job = self.cron.new(command=command)
		cron_job.minute.on(0)
		cron_job.hour.on(0)
		cron_job.day.on(1)
		cron_job.month.during(1,12)
		cron_job.enable()
		self.cron.write()
		if self.cron.render():
			print self.cron.render()
			return True

	def add_quarterly(self, name, user, command, environment=None):
		# Add a quarterly cron task
		cron_job = self.cron.new(command=command)
		cron_job.minute.on(0)
		cron_job.hour.on(0)
		cron_job.day.on(1)
		cron_job.month.on(3,6,9,12)
		cron_job.enable()
		self.cron.write()
		if self.cron.render():
			print self.cron.render()
			return True



cron_log_file = '~/cron.log'

# update facilities every Monday at 00.00 hrs
facilities_script = settings.BASE_DIR + 'utilities/auto_update_facility_list.py'
facilities_cmd = 'python' + facilities_script + '>>' + cron_log_file
CronManager().add_weekly(user='root', command=facilities_cmd, day=1, hour=0)

# update ovc_viral_load every Sunday at 00.00 hrs
viral_load_script = settings.BASE_DIR + 'utilities/auto_update_ovc_viralload.py'
viralload_cmd = 'python' + viral_load_script + '>>' + cron_log_file
CronManager().add_weekly(user='root', command=viralload_cmd, day=0, hour=0)