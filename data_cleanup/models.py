from django.db import models


class DataQuality(models.Model):
    """
    Demographic data data quality.
    """
    ovc_registration_id = models.IntegerField(primary_key=True)
    registration_date = models.DateTimeField()
    has_bcert = models.BooleanField()
    is_disabled = models.BooleanField()
    hiv_status = models.CharField(max_length=255)
    school_level = models.CharField(max_length=255)
    immunization_status = models.CharField(max_length=255)
    org_unique_id = models.CharField(max_length=255)
    exit_reason = models.CharField(max_length=255)
    exit_date = models.CharField(max_length=255)
    ovc_registration_created_at = models.CharField(max_length=255)
    ovc_registration_is_active = models.BooleanField()
    ovc_registration_is_void = models.BooleanField()
    caretaker_id = models.CharField(max_length=255)
    child_cbo_id = models.CharField(max_length=255)
    child_chv_id = models.CharField(max_length=255)
    person_id = models.CharField(max_length=255)
    art_status = models.CharField(max_length=255)
    reg_person_id = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    des_phone_number = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField()
    date_of_death = models.DateTimeField
    sex_id = models.CharField(max_length=255)
    is_void = models.BooleanField()
    reg_person_created_at = models.DateTimeField()
    created_by_id= models.IntegerField()
    age =  models.IntegerField()

    class Meta:
        managed= False
        db_table = 'data_quality_view'

    def __str__(self):
        return self.first_name



class Form1BServicesDataQuality(models.Model):
    """
    Combining demography data together with the other form 1b services.
    """
    id = models.CharField(max_length=255, primary_key=True)
    domain = models.CharField(max_length=255)
    entity = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    event_id = models.CharField(max_length=255) # Same as event on the ovc_care_events
    person_id = models.CharField(max_length=255)
    has_bcert = models.BooleanField()
    is_disabled = models.BooleanField()
    hiv_status = models.CharField(max_length=255)
    school_level = models.CharField(max_length=255)
    child_cbo_id = models.CharField(max_length=255)
    art_status =  models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    sex_id = models.CharField(max_length=255)
    service_provided = models.CharField(max_length=255)
    service_id = models.CharField(max_length=255)

    class Meta:
        managed= False
        db_table = 'data_quality_form1b'


class OVCCareServicesDataQuality(models.Model):
    """
    Combining demography data together with the other OVC Care services.
    """
    id = models.CharField(max_length=255, primary_key=True)
    ovc_care_events_person_id = models.CharField(max_length=255)
    has_bcert = models.BooleanField()
    is_disabled = models.BooleanField()
    hiv_status = models.CharField(max_length=255)
    school_level = models.CharField(max_length=255)
    child_cbo_id = models.CharField(max_length=255)
    art_status =  models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    age = models.IntegerField()
    service_provided = models.CharField(max_length=255)
    sex_id = models.CharField(max_length=255)

    class Meta:
        managed= False
        db_table = 'data_quality_ovc_care_services'