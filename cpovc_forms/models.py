from django.db import models
from django.utils import timezone
import datetime
import uuid
from cpovc_registry.models import (RegPerson, RegOrgUnit, AppUser)
from cpovc_main.models import (SchoolList)
from cpovc_ovc.models import (OVCHouseHold, OVCFacility)

# Create your models here.
class OVCBursary(models.Model):
    bursary_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    bursary_type = models.CharField(max_length=4, null=True)
    disbursement_date = models.DateField(default=timezone.now, null=True)
    amount = models.CharField(max_length=20, null=True)
    year = models.CharField(max_length=20, null=True)
    term = models.CharField(max_length=20, null=True)
    person = models.ForeignKey(RegPerson)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    created_by = models.IntegerField(null=True, default=404)

    class Meta:
        db_table = 'ovc_bursaryinfo'


class OVCCaseRecord(models.Model):
    # Make case_id primary key
    case_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case_serial = models.CharField(max_length=50, default='XXXX')
    # place_of_event = models.CharField(max_length=50)
    perpetrator_status = models.CharField(max_length=20, default='PKNW')
    perpetrator_first_name = models.CharField(max_length=50, null=True)
    perpetrator_other_names = models.CharField(max_length=50, null=True)
    perpetrator_surname = models.CharField(max_length=50, null=True)
    perpetrator_relationship_type = models.CharField(max_length=50, null=True)
    # case_nature = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=50)
    date_case_opened = models.DateField(default=datetime.date.today)
    case_reporter_first_name = models.CharField(max_length=50, null=True)
    case_reporter_other_names = models.CharField(max_length=50, null=True)
    case_reporter_surname = models.CharField(max_length=50, null=True)
    case_reporter_contacts = models.CharField(max_length=20, null=True)
    case_reporter = models.CharField(max_length=20, blank=True)
    court_name = models.CharField(max_length=200, null=True)
    court_number = models.CharField(max_length=50, null=True)
    police_station = models.CharField(max_length=200, null=True)
    ob_number = models.CharField(max_length=50, null=True)
    case_status = models.CharField(max_length=50, default='ACTIVE')
    referral_present = models.CharField(max_length=10, default='AYES')
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    parent_case_id = models.UUIDField(null=True)
    created_by = models.IntegerField(null=True, default=404)
    person = models.ForeignKey(RegPerson)
    case_remarks = models.CharField(max_length=1000, null=True)
    date_of_summon = models.DateField(null=True)
    summon_status = models.NullBooleanField(null=True, default=None)

    class Meta:
        db_table = 'ovc_case_record'


class OVCCaseGeo(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    report_subcounty = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='report_subcounty_fk')
    report_ward = models.CharField(max_length=100, null=True)
    report_village = models.CharField(max_length=100, null=True)
    report_orgunit = models.ForeignKey(RegOrgUnit, max_length=10, null=True)
    occurence_county = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='occurence_county_fk', on_delete=models.CASCADE)
    occurence_subcounty = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='occurence_subcounty_fk', on_delete=models.CASCADE)
    occurence_ward = models.CharField(max_length=100, blank=True)
    occurence_village = models.CharField(max_length=100, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_case_geo'


class OVCEconomicStatus(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    # family_status_id = models.CharField(max_length=100)
    household_economic_status = models.CharField(max_length=100)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_economic_status'


class OVCFamilyStatus(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    family_status = models.CharField(max_length=100)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_family_status'


class OVCHobbies(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    hobby = models.CharField(max_length=200)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_hobbies'


class OVCFriends(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    friend_firstname = models.CharField(max_length=50)
    friend_other_names = models.CharField(max_length=50)
    friend_surname = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_friends'


class OVCMedical(models.Model):
    medical_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    mental_condition = models.CharField(max_length=50)
    physical_condition = models.CharField(max_length=50)
    other_condition = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_medical'


class OVCMedicalSubconditions(models.Model):
    medicalsubcond_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    medical_id = models.ForeignKey(OVCMedical, on_delete=models.CASCADE)
    medical_condition = models.CharField(max_length=50)
    medical_subcondition = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_medical_subconditions'


class OVCCaseCategory(models.Model):
    case_category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    # case_category_id = models.CharField(max_length=10, primary_key=True)
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    case_category = models.CharField(max_length=4)
    case_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    date_of_event = models.DateField(default=timezone.now)
    place_of_event = models.CharField(max_length=4)
    case_nature = models.CharField(max_length=4)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_case_category'


class OVCCaseSubCategory(models.Model):
    case_sub_category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case_category = models.ForeignKey(OVCCaseCategory, on_delete=models.CASCADE)
    case_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    sub_category_id = models.CharField(max_length=4)
    person = models.ForeignKey(RegPerson)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_case_sub_category'


"""
class OVCInterventions(models.Model):
    inteventions_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    intervention = models.CharField(max_length=100)
    case_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_case_interventions'
"""


class OVCReferral(models.Model):
    refferal_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    refferal_actor_type = models.CharField(max_length=4)
    refferal_actor_specify = models.CharField(max_length=50)
    refferal_to = models.CharField(max_length=4)
    refferal_status = models.CharField(max_length=20, default='PENDING')
    refferal_startdate = models.DateField(default=datetime.date.today)
    refferal_enddate = models.DateField(null=True)
    # case_category = models.CharField(max_length=20, blank=True)
    case_category = models.ForeignKey(
        OVCCaseCategory, default=uuid.uuid1, editable=False, null=True, on_delete=models.CASCADE)
    referral_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_referrals'


class OVCNeeds(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    need_description = models.CharField(max_length=250)
    need_type = models.CharField(max_length=250)  # LongTerm/Immediate
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_needs'


class FormsLog(models.Model):
    form_log_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    form_type_id = models.CharField(max_length=250)
    form_id = models.CharField(max_length=50, default='XXXX')
    person = models.ForeignKey(RegPerson, null=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    timestamp_modified = models.DateTimeField(auto_now=True)
    app_user = models.IntegerField(null=True, default=404)

    # app_user = models.ForeignKey(AppUser, default=1)

    class Meta:
        db_table = 'forms_log'


class FormsAuditTrail(models.Model):
    """Model for Forms Audit."""
    transaction_id = models.AutoField(primary_key=True)
    form_id =  models.UUIDField(null=True)
    form_type_id = models.CharField(max_length=250)
    transaction_type_id = models.CharField(max_length=4, null=True, db_index=True)
    interface_id = models.CharField(max_length=4, null=True, db_index=True)
    timestamp_modified = models.DateTimeField(auto_now=True)
    app_user = models.ForeignKey(AppUser)
    ip_address = models.GenericIPAddressField(protocol='both')
    meta_data = models.TextField(null=True)

    class Meta:
        """Override table details."""
        db_table = 'forms_audit_trail'


class OVCPlacement(models.Model):
    placement_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    residential_institution_name = models.CharField(max_length=100, blank=True)
    admission_date = models.DateField(default=timezone.now, null=True)
    admission_type = models.CharField(max_length=4, blank=True)
    transfer_from = models.CharField(max_length=100, null=True)
    admission_reason = models.CharField(max_length=100, blank=True)
    holding_period = models.IntegerField(null=True)
    committing_period_units = models.CharField(max_length=4, null=True)
    committing_period = models.IntegerField(null=True)
    current_residential_status = models.CharField(max_length=4)
    has_court_committal_order = models.CharField(max_length=4)
    free_for_adoption = models.CharField(null=True, max_length=4)
    court_order_number = models.CharField(null=True, max_length=20)
    court_order_issue_date = models.DateField(default=timezone.now, null=True)
    committing_court = models.CharField(max_length=100, null=True)
    placement_notes = models.CharField(max_length=1000, null=True)
    ob_number = models.CharField(null=True, max_length=20)
    placement_type = models.CharField(
        max_length=10, default='Normal')  # Emergency/Normal
    person = models.ForeignKey(RegPerson)
    created_by = models.IntegerField(null=True, default=404)
    is_active = models.BooleanField(default=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_placement'


class OVCCaseEvents(models.Model):
    case_event_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    case_event_type_id = models.CharField(max_length=20)
    date_of_event = models.DateField(default=timezone.now)
    case_event_details = models.CharField(max_length=100)
    case_event_notes = models.CharField(max_length=1000, blank=True)
    case_event_outcome = models.CharField(max_length=250, null=True)
    next_hearing_date = models.DateField(null=True)  # For Court Adjournments
    next_mention_date = models.DateField(null=True)  # For Court Mentions
    plea_taken = models.CharField(max_length=4, null=True)  # For Plea Taken (Guilty/Not Guilty)
    application_outcome = models.CharField(max_length=4, null=True)  # For Application Outcome (Granted/Not Granted)
    placement_id = models.ForeignKey(OVCPlacement, null=True) # To track children who went to court from institutions
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    case_id = models.ForeignKey(OVCCaseRecord, null=True, on_delete=models.CASCADE)
    app_user = models.ForeignKey(AppUser, default=1)

    class Meta:
        db_table = 'ovc_case_events'


class OVCCaseEventServices(models.Model):
    service_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    service_provided = models.CharField(max_length=250)
    service_provider = models.CharField(max_length=250, null=True)
    place_of_service = models.CharField(max_length=250, null=True)
    date_of_encounter_event = models.DateField(default=timezone.now)
    case_event_id = models.ForeignKey(OVCCaseEvents, on_delete=models.CASCADE)
    service_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    timestamp_created = models.DateTimeField(default=timezone.now)
    case_category = models.ForeignKey(
        OVCCaseCategory, default=uuid.uuid1, editable=False, blank=True)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_case_event_encounters'


class OVCCaseEventCourt(models.Model):
    court_session_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    court_order = models.CharField(max_length=250, null=True)
    case_event_id = models.ForeignKey(OVCCaseEvents, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    case_category = models.ForeignKey(
        OVCCaseCategory, default=uuid.uuid1, editable=False, blank=True, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_case_event_court'


class OVCCaseEventSummon(models.Model):
    summon_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)

    honoured = models.BooleanField(default=False)
    honoured_date = models.DateField(null=True)
    summon_date = models.DateField(null=True)
    # summon_date_next = models.DateField(null=True)
    summon_note = models.CharField(max_length=250, null=True)
    # visit_date = models.DateField(null=True)
    case_event_id = models.ForeignKey(OVCCaseEvents, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    case_category = models.ForeignKey(
        OVCCaseCategory, default=uuid.uuid1, editable=False, null=True, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_case_event_summon'


class OVCCaseEventClosure(models.Model):
    closure_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    # case_status = models.CharField(max_length=20)
    case_outcome = models.CharField(max_length=4)
    date_of_case_closure = models.DateField(default=timezone.now)
    case_closure_notes = models.CharField(max_length=1000)
    transfer_to = models.ForeignKey(RegOrgUnit, max_length=10, null=True)
    # case_id = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    case_event_id = models.ForeignKey(OVCCaseEvents, on_delete=models.CASCADE)
    created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_case_event_closure'


class OVCReminders(models.Model):
    reminder_date = models.DateField(default=timezone.now)
    reminder_type = models.CharField(max_length=100)
    reminder_description = models.CharField(max_length=1000)
    reminder_status = models.CharField(max_length=10)
    person = models.ForeignKey(RegPerson)
    created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_reminders'


class OVCDocuments(models.Model):
    document_type = models.CharField(max_length=100)
    document_description = models.CharField(max_length=200)
    document_name = models.CharField(max_length=100, blank=True)
    document_dir = models.CharField(max_length=1000, blank=True)
    person = models.ForeignKey(RegPerson)
    created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_documents'


class OVCPlacementFollowUp(models.Model):
    placememt_followup_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    followup_type = models.CharField(max_length=100)
    followup_date = models.DateField(default=timezone.now)
    followup_details = models.CharField(max_length=1000, blank=True)
    followup_outcome = models.CharField(max_length=1000, blank=True)
    person = models.ForeignKey(RegPerson)
    placement_id = models.ForeignKey(OVCPlacement)
    created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_placement_followup'



class OVCEducationFollowUp(models.Model):
    education_followup_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    admitted_to_school = models.CharField(max_length=10)
    admission_to_school_date = models.DateField(
        default=timezone.now, null=True)
    education_comments = models.CharField(max_length=1000, null=True)

    # -- New ---
    school_id = models.ForeignKey(SchoolList, null=True)
    not_in_school_reason = models.CharField(max_length=4, null=True)
    school_admission_type = models.CharField(max_length=4, null=True)
    # ---------
    placement_id = models.ForeignKey(OVCPlacement, null=True)
    person = models.ForeignKey(RegPerson)
    created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_education_followup'


class OVCEducationLevelFollowUp(models.Model):
    admission_level = models.CharField(max_length=20, null=True)
    admission_sublevel = models.CharField(max_length=20, null=True)
    education_followup_id = models.ForeignKey(OVCEducationFollowUp)
    # created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_education_level_followup'


class OVCDischargeFollowUp(models.Model):
    discharge_followup_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    type_of_discharge = models.CharField(max_length=20)
    date_of_discharge = models.DateField(default=timezone.now, null=True)
    discharge_destination = models.CharField(max_length=20, null=True)
    reason_of_discharge = models.CharField(max_length=1000, blank=True)
    expected_return_date = models.DateField(null=True)
    actual_return_date = models.DateField(null=True)
    discharge_comments = models.CharField(max_length=1000, blank=True)
    created_by = models.IntegerField(null=True, default=404)
    placement_id = models.ForeignKey(OVCPlacement)
    person = models.ForeignKey(RegPerson)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_discharge_followup'


class OVCAdverseEventsFollowUp(models.Model):
    adverse_condition_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    adverse_condition_description = models.CharField(max_length=20)
    attendance_type = models.CharField(max_length=4, null=True)
    referral_type = models.CharField(max_length=4, null=True)
    adverse_event_date = models.DateField(default=timezone.now, null=True)
    placement_id = models.ForeignKey(OVCPlacement)
    person = models.ForeignKey(RegPerson)
    created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_adverseevents_followup'


class OVCAdverseEventsOtherFollowUp(models.Model):
    adverse_condition = models.CharField(max_length=20)
    adverse_condition_id = models.ForeignKey(OVCAdverseEventsFollowUp)
    # created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_adverseevents_other_followup'


"""
class OVCAdverseMedicalEventsFollowUp(models.Model):
    adverse_medical_condition = models.CharField(max_length=20)
    adverse_condition_id = models.ForeignKey(OVCAdverseEventsFollowUp)
    # created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_adverse_medical_events_followup'
"""


class OVCFamilyCare(models.Model):
    familycare_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    type_of_care = models.CharField(max_length=4)
    certificate_number = models.CharField(max_length=20, null=True)
    date_of_certificate_expiry = models.DateField(null=True)
    type_of_adoption = models.CharField(max_length=4, null=True)
    adoption_subcounty = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='adoption_subcounty_fk', null=True)
    adoption_country = models.CharField(max_length=20, null=True)
    residential_institution_name = models.ForeignKey(RegOrgUnit, related_name='residential_institution_name_fk', null=True)
    fostered_from = models.ForeignKey(RegOrgUnit, related_name='fostered_from_fk', null=True)
    date_of_adoption = models.DateField(default=timezone.now, null=True)
    court_name = models.CharField(max_length=100, null=True)
    court_file_number = models.CharField(max_length=20, null=True)
    # adoption_startdate = models.CharField(max_length=20)
    parental_status = models.CharField(max_length=4, null=True)
    children_office = models.ForeignKey(RegOrgUnit, related_name='children_office_fk', null=True)
    contact_person = models.CharField(max_length=20, null=True)
    adopting_mother_firstname = models.CharField(max_length=20, null=True)
    adopting_mother_othernames = models.CharField(max_length=20, null=True)
    adopting_mother_surname = models.CharField(max_length=20, null=True)
    adopting_mother_othernames = models.CharField(max_length=20, null=True)
    adopting_mother_idnumber = models.CharField(max_length=20, null=True)
    adopting_mother_contacts = models.CharField(max_length=20, null=True)
    adopting_father_firstname = models.CharField(max_length=20, null=True)
    adopting_father_othernames = models.CharField(max_length=20, null=True)
    adopting_father_surname = models.CharField(max_length=20, null=True)
    adopting_father_othernames = models.CharField(max_length=20, null=True)
    adopting_father_idnumber = models.CharField(max_length=20, null=True)
    adopting_father_contacts = models.CharField(max_length=20, null=True)
    adopting_agency = models.CharField(max_length=20, null=True)
    adoption_remarks = models.CharField(max_length=1000, null=True)
    person = models.ForeignKey(RegPerson)
    created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    # children_office/contact_person/parental_status

    class Meta:
        db_table = 'ovc_family_care'


## ---------------------------- OVC Models --------------------------------------#


class OVCCareEvents(models.Model):
    event = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    event_type_id = models.CharField(max_length=10)
    event_counter = models.IntegerField(default=0)
    event_score = models.IntegerField(null=True, default=0)
    date_of_event = models.DateField(default=timezone.now)
    date_of_previous_event = models.DateTimeField(null=True)
    created_by = models.IntegerField(null=True, default=404)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)
    # app_user = models.ForeignKey(AppUser, default=1)
    person = models.ForeignKey(RegPerson, null=True)
    house_hold = models.ForeignKey(OVCHouseHold, null=True)

    class Meta:
        db_table = 'ovc_care_events'


class OVCCareAssessment(models.Model):
    """ This table will hold OVC Assessment Data """

    assessment_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    domain = models.CharField(max_length=4)
    service = models.CharField(max_length=4)
    service_status = models.CharField(max_length=7)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    service_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_care_assessment'


class OVCCarePriority(models.Model):
    """ This table will hold OVC Priority Data """

    priority_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    domain = models.CharField(max_length=4)
    service = models.CharField(max_length=4)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    service_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_care_priority'


class OVCCareServices(models.Model):
    """ This table will hold Services Data """

    service_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    service_provided = models.CharField(max_length=250)
    service_provider = models.CharField(max_length=250, null=True)
    domain = models.CharField(max_length=4, null=True)
    place_of_service = models.CharField(max_length=250, null=True)
    date_of_encounter_event = models.DateField(default=timezone.now, null=True)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    service_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_care_services'


class OVCCareEAV(models.Model):
    """ This table will hold HHVA data and Domain Evaluation data """

    eav_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    entity = models.CharField(max_length=5)
    attribute = models.CharField(max_length=5)
    value = models.CharField(max_length=25)
    value_for = models.CharField(max_length=10, null=True)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid1, editable=False)

    class Meta:
        db_table = 'ovc_care_eav'


class OVCCareF1B(models.Model):
    """ This table will hold Form 1B data """

    form_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    domain = models.CharField(max_length=5)
    entity = models.CharField(max_length=5)
    value = models.SmallIntegerField(default=1)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_care_f1b'


class ListBanks(models.Model):
    """List all Banks in Kenya."""
    bank_name = models.CharField(max_length=150)
    bank_code = models.CharField(max_length=10)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'list_bank'
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.bank_name


class OVCGokBursary(models.Model):
    """"Model to save all GoK Bursary application."""
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    county = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='child_county')
    constituency = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='child_constituency')
    person = models.ForeignKey(RegPerson)
    sub_county = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    sub_location = models.CharField(max_length=100, null=True)
    village = models.CharField(max_length=100)
    nearest_school = models.CharField(max_length=100, null=True)
    nearest_worship = models.CharField(max_length=100, null=True)
    in_school = models.BooleanField(default=True)
    school_class = models.CharField(max_length=50)
    primary_school = models.CharField(max_length=150)
    school_marks = models.IntegerField()
    father_names = models.CharField(max_length=100)
    father_alive = models.BooleanField(default=True)
    father_telephone = models.CharField(max_length=20, null=True)
    mother_names = models.CharField(max_length=100)
    mother_alive = models.BooleanField(default=True)
    mother_telephone = models.CharField(max_length=20, null=True)
    guardian_names = models.CharField(max_length=100, null=True)
    guardian_telephone = models.CharField(max_length=20, null=True)
    guardian_relation = models.CharField(max_length=20, null=True)
    same_household = models.BooleanField(default=True)
    father_chronic_ill = models.BooleanField(default=True)
    father_chronic_illness = models.CharField(max_length=100, null=True)
    father_disabled = models.BooleanField(default=True)
    father_disability = models.CharField(max_length=100, null=True)
    father_pension = models.BooleanField(default=True)
    father_occupation = models.CharField(max_length=100, null=True)
    mother_chronic_ill = models.BooleanField(default=True)
    mother_chronic_illness = models.CharField(max_length=100, null=True)
    mother_disabled = models.BooleanField(default=True)
    mother_disability = models.CharField(max_length=100, null=True)
    mother_pension = models.BooleanField(default=True)
    mother_occupation = models.CharField(max_length=100, null=True)
    fees_amount = models.IntegerField()
    fees_balance = models.IntegerField()
    school_secondary = models.CharField(max_length=150)
    school_principal = models.CharField(max_length=150)
    school_county = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='school_county')
    school_constituency = models.ForeignKey(
        'cpovc_main.SetupGeography', related_name='school_constituency')
    school_sub_county = models.CharField(max_length=100, null=True)
    school_location = models.CharField(max_length=100, null=True)
    school_sub_location = models.CharField(max_length=100, null=True)
    school_village = models.CharField(max_length=100, null=True)
    school_telephone = models.CharField(max_length=20, null=True)
    school_email = models.CharField(max_length=100, null=True)
    school_type = models.CharField(max_length=5)
    school_category = models.CharField(max_length=5)
    school_enrolled = models.CharField(max_length=5)
    school_bank = models.ForeignKey(ListBanks)
    school_bank_branch = models.CharField(max_length=100)
    school_bank_account = models.CharField(max_length=50)
    school_recommend_by = models.CharField(max_length=5)
    school_recommend_date = models.DateField()
    chief_recommend_by = models.CharField(max_length=5)
    chief_recommend_date = models.DateField()
    chief_telephone = models.CharField(max_length=5)
    csac_approved = models.BooleanField(default=True)
    approved_amount = models.IntegerField()
    ssco_name = models.CharField(max_length=100)
    scco_signed = models.BooleanField(default=True)
    scco_sign_date = models.DateField()
    csac_chair_name = models.CharField(max_length=100)
    csac_signed = models.BooleanField(default=True)
    csac_sign_date = models.DateField()
    app_user = models.ForeignKey(AppUser)
    application_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'bursary_application'
        verbose_name = 'GoK Bursary'
        verbose_name_plural = 'GoK Bursaries'

    def __unicode__(self):
        """To be returned by admin actions."""
        return str(self.application_id)


'''
Classes below were added due to ovc case management
'''


class OVCCareForms(models.Model):
    form_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_void = models.BooleanField(default=False)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_care_forms'

    def __unicode__(self):
        return str(self.form_id)


class OVCCareBenchmarkScore(models.Model):

    bench_mark_score_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    household = models.ForeignKey(OVCHouseHold, on_delete=models.CASCADE)
    bench_mark_1 = models.IntegerField(default=0)
    bench_mark_2 = models.IntegerField(default=0)
    bench_mark_3 = models.IntegerField(default=0)
    bench_mark_4 = models.IntegerField(default=0)
    bench_mark_5 = models.IntegerField(default=0)
    bench_mark_6 = models.IntegerField(default=0)
    bench_mark_7 = models.IntegerField(default=0)
    bench_mark_8 = models.IntegerField(default=0)
    bench_mark_9 = models.IntegerField(default=0)
    bench_mark_10 = models.IntegerField(default=0)
    bench_mark_11 = models.IntegerField(default=0)
    bench_mark_12 = models.IntegerField(default=0)
    bench_mark_13 = models.IntegerField(default=0)
    bench_mark_14 = models.IntegerField(default=0)
    bench_mark_15 = models.IntegerField(default=0)
    bench_mark_16 = models.IntegerField(default=0)
    bench_mark_17 = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    care_giver = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)
    date_of_event = models.DateField(default=timezone.now)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.bench_mark_score_id)

    class Meta:
        db_table = 'ovc_care_benchmark_score'

    def __unicode__(self):
        return str(self.bench_mark_score_id)


class OVCCareCpara(models.Model):
    cpara_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(RegPerson, on_delete=models.CASCADE, related_name='cpara_caregiver')
    question_code = models.CharField(max_length=10, null=False, blank=True)
    question = models.ForeignKey('OVCCareQuestions')
    answer = models.CharField(max_length=15)
    household = models.ForeignKey(OVCHouseHold, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    date_of_event = models.DateField()
    date_of_previous_event =models.DateField(null=True, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    timestamp_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.answer

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.question_code = self.question.code
        super(OVCCareCpara, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'ovc_care_cpara'

    def __unicode__(self):
        return str(self.cpara_id)


class OVCCareWellbeing(models.Model):
    well_being_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(RegPerson, on_delete=models.CASCADE, related_name='wellbeing_caregiver')
    question_code = models.CharField(max_length=10, null=False, blank=True)
    question = models.ForeignKey('OVCCareQuestions')
    answer = models.CharField(max_length=250)
    household = models.ForeignKey(OVCHouseHold, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=5)
    domain = models.CharField(max_length=10)
    is_void = models.BooleanField(default=False)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    date_of_event = models.DateField()
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.answer

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.question_code = self.question.code
        super(OVCCareWellbeing, self).save(force_insert, force_update, using, update_fields)


    class Meta:
        db_table = 'ovc_care_well_being'

    def __unicode__(self):
        return str(self.well_being_id)


class OVCCareCasePlan(models.Model):
    case_plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain = models.CharField(max_length=50)
    goal = models.CharField(max_length=255)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(RegPerson, on_delete=models.CASCADE, related_name='caseplan_caregiver')
    household = models.ForeignKey(OVCHouseHold, on_delete=models.CASCADE)
    need = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    # cp_service = models.ForeignKey('cpovc_main.SetupList', on_delete=models.CASCADE)
    cp_service = models.CharField(max_length=10)
    responsible = models.CharField(max_length=50)
    completion_date = models.DateField(default=timezone.now)
    actual_completion_date = models.DateField(default=timezone.now)
    results = models.CharField(max_length=300)
    reasons = models.CharField(max_length=300)
    form = models.ForeignKey(OVCCareForms)
    date_of_event = models.DateField()
    date_of_previous_event =models.DateField(null=True, blank=True)
    case_plan_status=models.CharField(max_length=5)
    initial_caseplan=models.BooleanField(default=True)
    is_void = models.BooleanField(default=False)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.results

    class Meta:
        db_table = 'ovc_care_case_plan'

    def __unicode__(self):
        return str(self.case_plan_id)


class OVCHouseholdDemographics(models.Model):
    household_demographics_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    household = models.ForeignKey(OVCHouseHold, on_delete=models.CASCADE)
    key = models.CharField(max_length=15)
    male = models.IntegerField(default=0)
    female = models.IntegerField(default=0)
    is_void = models.BooleanField(default=False)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_household_demographics'

    def __unicode__(self):
        return str(self.household_demographics_id)


class OVCExplanations(models.Model):
    explanation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey('OVCCareQuestions')
    comment = models.CharField(max_length=255)
    form = models.ForeignKey(OVCCareForms)
    event = models.ForeignKey(OVCCareEvents, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)
    timestamp_updated = models.DateTimeField(auto_now=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_explanations'

    def __unicode__(self):
        return str(self.explanation_id)


class OVCGoals(models.Model):
    goal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson)
    goal = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    event = models.ForeignKey(OVCCareEvents)
    is_void = models.BooleanField(default=False)
    date_of_event = models.DateField()
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_goals'

    def __unicode__(self):
        return str(self.goal_id)


class OVCReferrals(models.Model):
    referral_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(RegPerson)
    referral_date = models.DateField(default=timezone.now)
    service = models.CharField(max_length=20)
    institution = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=50)
    event = models.ForeignKey(OVCCareEvents)
    completed = models.BooleanField(default=False)
    outcome = models.CharField(max_length=255)
    is_void = models.BooleanField(default=False)
    date_of_event = models.DateField()
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_cp_referrals'

    def __unicode__(self):
        return str(self.referral_id)


class OVCMonitoring(models.Model):
    monitoring_id = models.AutoField(primary_key=True)
    household = models.ForeignKey(OVCHouseHold, on_delete=models.CASCADE)
    hiv_status_knowledge = models.CharField(max_length=5)
    viral_suppression = models.CharField(max_length=5)
    hiv_prevention = models.CharField(max_length=5)
    undernourished = models.CharField(max_length=5)
    access_money = models.CharField(max_length=5)
    violence = models.CharField(max_length=5)
    caregiver = models.CharField(max_length=5)
    school_attendance = models.CharField(max_length=5)
    school_progression = models.CharField(max_length=5)
    cp_achievement = models.CharField(max_length=5)
    case_closure = models.CharField(max_length=5)
    case_closure_checked =  models.CharField(max_length=5)
    event = models.ForeignKey(OVCCareEvents)
    quarter = models.CharField(max_length=10, null=True, blank=True)
    is_void = models.BooleanField(default=False)
    event_date = models.DateField()
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_monitoring'

    def __unicode__(self):
        return str(self.monitoring_id)


class OVCHivStatus(models.Model):
    hiv_status_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(RegPerson)
    hiv_status = models.CharField(max_length=10)
    event = models.ForeignKey(OVCCareEvents)
    is_void = models.BooleanField(default=False)
    date_of_event = models.DateField()
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_hiv_status'

    def __unicode__(self):
        return str(self.hiv_status_id)


class OVCCareQuestions(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    code = models.CharField(max_length=5)
    question = models.CharField(max_length=55)
    domain = models.CharField(max_length=10)
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, null=False)
    form = models.ForeignKey(OVCCareForms)
    is_void = models.BooleanField(default=False)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.code

    class Meta:
        db_table = 'ovc_care_questions'

    def __unicode__(self):
        return str(self.question_id)


class OVCHIVRiskScreening(models.Model):
    risk_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson)
    test_done_when= models.NullBooleanField()
    test_donewhen_result=models.NullBooleanField()
    caregiver_know_status= models.NullBooleanField()
    caregiver_knowledge_yes=models.CharField(max_length=50, null=True)
    parent_PLWH= models.NullBooleanField()
    child_sick_malnourished= models.NullBooleanField()
    child_sexual_abuse= models.NullBooleanField()
    adol_sick= models.NullBooleanField()
    adol_sexual_abuse= models.NullBooleanField()
    sex= models.NullBooleanField()
    sti= models.NullBooleanField()
    hiv_test_required= models.NullBooleanField()
    parent_consent_testing= models.NullBooleanField()
    parent_consent_date=models.DateTimeField(default=timezone.now, null=True) ###date new 1
    referral_made= models.NullBooleanField()
    referral_made_date=models.DateTimeField(default=datetime.datetime.now(), null=True)####
    referral_completed= models.NullBooleanField()
    referral_completed_date=models.DateTimeField(default=timezone.now, null=True)### date new 2
    not_completed=models.CharField(max_length=50)
    test_result=models.CharField(max_length=20, null=True)
    art_referral= models.NullBooleanField()
    art_referral_date=models.DateTimeField(default=datetime.datetime.now(), null=True)#### date
    art_referral_completed= models.NullBooleanField()
    art_referral_completed_date=models.DateTimeField(default=datetime.datetime.now(), null=True)#### date
    facility_code = models.CharField(max_length=10, null=True)
    event = models.ForeignKey(OVCCareEvents)
    is_void = models.NullBooleanField()
    date_of_event = models.DateField(default=datetime.datetime.now(), null=True)### date 
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_risk_screening'
    def __unicode__(self):
        return str(self.risk_id)


class OVCHIVManagement(models.Model):
    adherence_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson)
    hiv_confirmed_date = models.DateTimeField(null=False)
    treatment_initiated_date = models.DateTimeField(null=False)
    baseline_hei=models.CharField(max_length=100, null=False)
    firstline_start_date = models.DateTimeField(null=False)
    substitution_firstline_arv = models.BooleanField(default=False)
    substitution_firstline_date = models.DateTimeField(default=datetime.datetime.now())
    switch_secondline_arv = models.BooleanField(default=False)
    switch_secondline_date = models.DateTimeField(null=True)
    switch_thirdline_arv = models.BooleanField(default=False)
    switch_thirdline_date = models.DateTimeField(null=True)
    visit_date = models.DateTimeField(null=False)
    duration_art = models.CharField(max_length=3, null=True)
    height = models.CharField(max_length=3, null=True)
    muac = models.CharField(max_length=20, null=True)
    adherence = models.CharField(max_length=20, null=False)
    adherence_drugs_duration = models.CharField(max_length=3, null=True)
    adherence_counselling = models.CharField(max_length=20, null=True)
    treatment_suppoter= models.CharField(max_length=100, null=True)##################
    treatment_supporter_relationship = models.CharField(max_length=20, null=True)
    treatment_supporter_gender = models.CharField(max_length=11, null=True)
    treatment_supporter_age = models.CharField(max_length=11, null=True)
    treament_supporter_hiv = models.CharField(max_length=100, null=True)
    viral_load_results = models.CharField(max_length=7, null=True)
    viral_load_date = models.DateTimeField(null=False)############
    detectable_viralload_interventions = models.CharField(max_length=50, null=True)
    disclosure = models.CharField(max_length=20, null=True)
    muac_score = models.CharField(max_length=20, null=True)
    bmi = models.CharField(max_length=20, null=True)
    nutritional_support = models.CharField(max_length=50, null=True)
    support_group_status = models.CharField(max_length=11, null=True)
    nhif_enrollment = models.BooleanField(default=False)
    support_group_enrollment = models.BooleanField(default=False)
    nhif_status = models.CharField(max_length=11, null=True)
    referral_services = models.CharField(max_length=100, null=True)
    nextappointment_date = models.DateField(null=True)
    peer_educator_name = models.CharField(max_length=100, null=True)
    peer_educator_contact = models.CharField(max_length=20, null=True)
    event = models.ForeignKey(OVCCareEvents)
    is_void = models.BooleanField(default=False)
    date_of_event = models.DateField()
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ovc_hiv_management'

    def __unicode__(self):
            return str(self.adherence_id)
