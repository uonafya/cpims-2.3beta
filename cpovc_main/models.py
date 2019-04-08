"""Main CPIMS models."""
import base64
from django.db import models
from django.utils import timezone
from cpovc_registry.models import RegPerson
import uuid


class SchoolList(models.Model):
    """List of Schools model."""

    # school_id = models.IntegerField(null=True, default=0)
    school_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    school_name = models.CharField(max_length=255)
    # level_of_education = models.CharField(max_length=255, null=True)
    school_subcounty = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='school_subcounty_fk',
        on_delete=models.CASCADE)
    school_ward = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='school_ward_fk',
        on_delete=models.CASCADE)
    type_of_school = models.CharField(max_length=26, null=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, default=404)

    class Meta:
        """Override some params."""

        db_table = 'school_list'


class FacilityList(models.Model):
    """Master Facility list model."""

    facility_code = models.IntegerField()
    facility_name = models.CharField(max_length=255)
    county_id = models.IntegerField()
    county_name = models.CharField(max_length=255)
    subcounty_id = models.IntegerField()
    subcounty_name = models.CharField(max_length=255)
    latitude = models.DecimalField(decimal_places=5, max_digits=10)
    longitude = models.DecimalField(decimal_places=5, max_digits=10)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'facility_list'


class SetupGeography(models.Model):
    """List of Geographical areas of Kenya."""

    area_id = models.IntegerField(primary_key=True)
    area_type_id = models.CharField(max_length=50)
    area_name = models.CharField(max_length=100)
    area_code = models.CharField(max_length=10, null=True)
    parent_area_id = models.IntegerField(null=True)
    area_name_abbr = models.CharField(max_length=5, null=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'list_geo'
        verbose_name = 'Setup Geography'
        verbose_name_plural = 'Setup Geographies'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s - %s' % (self.area_type_id, self.area_name)


class SetupList(models.Model):
    """List used for drop downs and other selections."""

    item_id = models.CharField(max_length=4)
    item_description = models.CharField(max_length=255)
    item_description_short = models.CharField(max_length=26, null=True)
    item_category = models.CharField(max_length=255, null=True, blank=True)
    item_sub_category = models.CharField(max_length=255, null=True, blank=True)
    the_order = models.IntegerField(null=True)
    user_configurable = models.BooleanField(default=False)
    sms_keyword = models.BooleanField(default=False)
    is_void = models.BooleanField(default=False)
    field_name = models.CharField(max_length=200, null=True, blank=True)
    timestamp_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override some params."""

        db_table = 'list_general'


class Forms(models.Model):
    """Forms model."""

    form_guid = models.CharField(max_length=64)
    form_title = models.CharField(max_length=255, null=True)
    form_type_id = models.CharField(max_length=4, null=True)
    form_subject_id = models.IntegerField(null=True, blank=False)
    form_area_id = models.IntegerField(null=True)
    date_began = models.DateField(null=True)
    date_ended = models.DateField(null=True)
    date_filled_paper = models.DateField(null=True)
    person_id_filled_paper = models.IntegerField(null=True)
    org_unit_id_filled_paper = models.IntegerField(null=True)
    capture_site_id = models.IntegerField(null=True, blank=True)
    timestamp_created = models.DateTimeField(null=True)
    user_id_created = models.CharField(max_length=9, null=True)
    timestamp_updated = models.DateTimeField(null=True)
    user_id_updated = models.CharField(max_length=9, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'forms'


class ListQuestions(models.Model):
    """List of questions used by forms."""

    question_text = models.CharField(max_length=255, null=True, blank=True)
    question_code = models.CharField(max_length=50)
    form_type_id = models.CharField(max_length=4, null=True, blank=True)
    answer_type_id = models.CharField(max_length=4, null=True, blank=True)
    answer_set_id = models.IntegerField(db_index=True, null=True)
    the_order = models.IntegerField(db_index=True, null=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'list_questions'


class ListAnswers(models.Model):
    """List of all answers used by questions in forms."""

    answer_set_id = models.IntegerField(db_index=True, null=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    the_order = models.IntegerField(db_index=True, null=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'list_answers'


class FormGenAnswers(models.Model):
    """Link to questions and answers for the forms."""

    form = models.ForeignKey(Forms)
    question = models.ForeignKey(ListQuestions)
    answer = models.ForeignKey(ListAnswers, null=True)

    class Meta:
        """Override some params."""

        db_table = 'form_gen_answers'


class FormGenText(models.Model):
    """Text used the questions and corresponding questions."""

    form = models.ForeignKey(Forms)
    question = models.ForeignKey(ListQuestions)
    answer_text = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        """Override some params."""

        db_table = 'form_gen_text'


class FormGenDates(models.Model):
    """Keed dates for forms and questions."""

    form = models.ForeignKey(Forms)
    question = models.ForeignKey(ListQuestions)
    answer_date = models.DateField()

    class Meta:
        """Override some params."""

        db_table = 'form_gen_dates'


class FormGenNumeric(models.Model):
    """Track form and questions with answers."""

    form = models.ForeignKey(Forms)
    question = models.ForeignKey(ListQuestions)
    answer = models.DecimalField(null=True, decimal_places=1, max_digits=10)

    class Meta:
        """Override some params."""

        db_table = 'form_gen_numeric'


class AdminUploadForms(models.Model):
    """Track admin form uploads."""

    form = models.ForeignKey(Forms)
    timestamp_uploaded = models.DateTimeField(null=True)

    class Meta:
        """Override some params."""

        db_table = 'admin_upload_forms'


class FormPersonParticipation(models.Model):
    """Form participation details."""

    form = models.ForeignKey(Forms)
    workforce_or_beneficiary_id = models.CharField(max_length=15)
    participation_level_id = models.CharField(max_length=4, null=True,
                                              blank=True)

    class Meta:
        """Override some params."""

        db_table = 'form_person_participation'


class FormOrgUnitContributions(models.Model):
    """Org unit contributions details."""

    form = models.ForeignKey(Forms)
    org_unit_id = models.CharField(max_length=7)
    contribution_id = models.CharField(max_length=4)
    # TODO part of composite key - org_unit_id and contrib_id

    class Meta:
        """Override some params."""

        db_table = 'form_org_unit_contribution'


class FormResChildren(models.Model):
    """Residential institution details."""

    form = models.ForeignKey(Forms, null=True)
    child_person_id = models.IntegerField(null=True, blank=True)
    institution_id = models.IntegerField(null=True, blank=True)
    residential_status_id = models.CharField(max_length=4, null=True,
                                             blank=True)
    court_committal_id = models.CharField(max_length=4, null=True, blank=True)
    family_status_id = models.CharField(max_length=4, null=True, blank=True)
    date_admitted = models.DateField(null=True, blank=True)
    date_left = models.DateField(null=True, blank=True)
    sms_id = models.IntegerField(null=True, blank=True)

    class Meta:
        """Override some params."""

        db_table = 'form_res_children'


class FormResWorkforce(models.Model):
    """Forms and work force relations."""

    form = models.ForeignKey(Forms)
    workforce_id = models.IntegerField(null=True, blank=True)
    institution_id = models.IntegerField(null=True, blank=True)
    position_id = models.CharField(max_length=4, null=True, blank=True)
    full_part_time_id = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        """Override some params."""

        db_table = 'form_res_workforce'


class AdminPreferences(models.Model):
    """Admin preferences settings details."""

    person = models.ForeignKey(RegPerson)
    preference_id = models.CharField(max_length=4)

    class Meta:
        """Override some params."""

        db_table = 'admin_preferences'


class CoreAdverseConditions(models.Model):
    """For adverse conditions tracking of case."""

    beneficiary_person = models.ForeignKey(RegPerson,
                                           related_name='adverse_beneficiary')
    adverse_condition_id = models.CharField(max_length=4)
    is_void = models.BooleanField(default=False)
    sms_id = models.IntegerField(null=True)
    form_id = models.IntegerField(null=True)

    class Meta:
        """Override some params."""

        db_table = 'core_adverse_conditions'


class CoreServices(models.Model):
    """For core services tracking of case."""

    workforce_person = models.ForeignKey(RegPerson,
                                         related_name='service_workforce')
    beneficiary_person = models.ForeignKey(RegPerson,
                                           related_name='service_beneficiary')
    encounter_date = models.DateField()
    core_item_id = models.CharField(max_length=4)
    sms_id = models.IntegerField(null=True)
    form_id = models.IntegerField(null=True)

    class Meta:
        """Override some params."""

        db_table = 'core_services'


class CoreEncounters(models.Model):
    """Core encouters for cases."""

    workforce_person = models.ForeignKey(RegPerson,
                                         related_name='encounter_workforce')
    beneficiary_person = models.ForeignKey(
        RegPerson, related_name='encounter_beneficiary')
    encounter_date = models.DateField()
    org_unit_id = models.IntegerField()
    area_id = models.IntegerField()
    encounter_type_id = models.CharField(max_length=4)
    sms_id = models.IntegerField(null=True)
    form_id = models.IntegerField(null=True)

    class Meta:
        """Override some params."""

        db_table = 'core_encounters'
        # unique_together = ("workforce_person", "beneficiary_person",
        # "encounter_date", "form_id")


class CoreEncountersNotes(models.Model):
    """Forms core encounters notes."""

    encounter = models.ForeignKey(CoreEncounters)
    form_id = models.IntegerField()
    workforce_person = models.ForeignKey(RegPerson,
                                         related_name='encounter_n_workforce')
    beneficiary_person = models.ForeignKey(
        RegPerson, related_name='encounter_n_beneficiary')
    encounter_date = models.DateField()
    note_type_id = models.CharField(max_length=4)
    note = models.CharField(max_length=255)

    class Meta:
        """Override some params."""

        db_table = 'form_encounters_notes'


class AdminCaptureSites(models.Model):
    """For tracking capture sites."""

    org_unit_id = models.IntegerField(null=True)
    capture_site_name = models.CharField(max_length=255, null=True, blank=True)
    date_installed = models.DateField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'admin_capture_sites'


class AdminDownload(models.Model):
    """Tracking all admin downloads."""

    capture_site_id = models.IntegerField(null=True, blank=True)
    section_id = models.CharField(max_length=4, null=True)
    timestamp_started = models.DateTimeField(null=True)
    timestamp_completed = models.DateTimeField(null=True)
    number_records = models.IntegerField(null=True)
    request_id = models.CharField(max_length=64, null=True)
    success = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'admin_download'


class CaptureTaskTracker(models.Model):
    """Capture tasks tracker."""

    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=64, null=True)
    operation = models.CharField(max_length=8, null=True)
    timestamp_started = models.DateTimeField(default=timezone.now)
    timestamp_completed = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'admin_task_tracker'


class ListReports(models.Model):
    """Listing of all reports."""

    report_code = models.CharField(max_length=100, null=True, blank=True)
    report_title_short = models.CharField(max_length=255, null=True)
    report_title_long = models.CharField(max_length=255, null=True)

    class Meta:
        """Override some params."""

        db_table = 'list_reports'


class ListReportsParameters(models.Model):
    """Reports parameters."""

    report = models.ForeignKey(ListReports, null=True)
    parameter = models.CharField(max_length=50, null=True, blank=True)
    filter = models.CharField(max_length=50, null=True, blank=True)
    initially_visible = models.BooleanField(default=False)
    label = models.CharField(max_length=100, null=True, blank=True)
    tip = models.CharField(max_length=255, null=True, blank=True)
    required = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'list_reports_parameter'


class ReportsSets(models.Model):
    """All reports sets."""

    set_name = models.CharField(max_length=70)
    set_type_id = models.CharField(max_length=4, default='SORG')
    user_id_created = models.IntegerField()

    class Meta:
        """Override some params."""

        db_table = 'reports_sets'


class ReportsSetsOrgUnits(models.Model):
    """Reports for Org units."""

    set = models.ForeignKey(ReportsSets)
    org_unit_id = models.IntegerField()

    class Meta:
        """Override some params."""

        db_table = 'reports_sets_org_unit'
        unique_together = ("set", "org_unit_id")


class RegTemp(models.Model):
    """For handling temp data."""

    user_id = models.IntegerField()
    page_id = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    _data = models.TextField(
        db_column='page_data',
        blank=True)

    def set_data(self, data):
        """Encode before saving."""
        self._data = base64.encodestring(data)

    def get_data(self):
        """"Decode after getting."""
        return base64.decodestring(self._data)

    data = property(get_data, set_data)

    class Meta:
        """Override some params."""

        db_table = 'reg_temp_data'
