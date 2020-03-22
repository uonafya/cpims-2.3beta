# import uuid
from django.db import models
from django.utils import timezone
from cpovc_registry.models import RegOrgUnit, RegPerson, RegPersonsTypes
from cpovc_forms.models import OVCCaseRecord, OVCPlacement
from cpovc_main.models import SetupGeography


class RPTCaseLoad(models.Model):
    """Model for Organisational Units details."""

    case = models.ForeignKey(OVCCaseRecord)
    case_serial = models.CharField(max_length=50, null=False)
    case_reporter_id = models.CharField(max_length=4)
    case_reporter = models.CharField(max_length=250)
    case_perpetrator_id = models.CharField(max_length=4, null=True)
    case_perpetrator = models.CharField(max_length=250, null=True)
    case_category_id = models.CharField(max_length=4)
    case_category = models.CharField(max_length=250)
    date_of_event = models.DateField(default=timezone.now)
    place_of_event_id = models.CharField(max_length=4)
    place_of_event = models.CharField(max_length=250)
    person_gender_id = models.CharField(max_length=4)
    person_gender = models.CharField(max_length=10)
    person_dob = models.DateField(default=timezone.now, null=True)
    report_county = models.ForeignKey(
        SetupGeography, related_name='rpt_county')
    report_county_name = models.CharField(max_length=250, null=True)
    report_subcounty = models.ForeignKey(
        SetupGeography, related_name='rpt_subcounty')
    report_subcounty_name = models.CharField(max_length=250, null=True)
    report_orgunit = models.ForeignKey(RegOrgUnit)
    report_orgunit_name = models.CharField(max_length=250, null=True)
    case_status = models.IntegerField(null=False)
    case_intervention_id = models.CharField(max_length=4, null=True)
    case_intervention = models.CharField(max_length=250, null=True)
    person = models.ForeignKey(RegPerson)
    case_date = models.DateField(null=True, default=timezone.now)
    system_date = models.DateField(null=True, default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'rpt_case_load'
        verbose_name = 'Protection Case data'
        verbose_name_plural = 'Protection Cases data'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.case_serial


class SIPopulation(OVCPlacement):
    class Meta:
        proxy = True
        verbose_name = 'SI Population'
        verbose_name_plural = 'SI Populations'


class CCIPopulation(OVCPlacement):
    class Meta:
        proxy = True
        verbose_name = 'CCI Population'
        verbose_name_plural = 'CCI Populations'


class SystemUsage(RegPersonsTypes):
    class Meta:
        proxy = True
        verbose_name = 'System Usage'
        verbose_name_plural = 'System Usages'
