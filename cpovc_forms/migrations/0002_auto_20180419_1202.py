# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_main', '0002_auto_20180419_1202'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cpovc_forms', '0001_initial'),
        ('cpovc_ovc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovcreminders',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcreferral',
            name='case_category',
            field=models.ForeignKey(default=uuid.uuid1, editable=False, to='cpovc_forms.OVCCaseCategory', null=True),
        ),
        migrations.AddField(
            model_name='ovcreferral',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovcreferral',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcplacementfollowup',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcplacementfollowup',
            name='placement_id',
            field=models.ForeignKey(to='cpovc_forms.OVCPlacement'),
        ),
        migrations.AddField(
            model_name='ovcplacement',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcneeds',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovcneeds',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcmedicalsubconditions',
            name='medical_id',
            field=models.ForeignKey(to='cpovc_forms.OVCMedical'),
        ),
        migrations.AddField(
            model_name='ovcmedicalsubconditions',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcmedical',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovcmedical',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovchobbies',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovchobbies',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcfriends',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovcfriends',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcfamilystatus',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovcfamilystatus',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='adoption_subcounty',
            field=models.ForeignKey(related_name='adoption_subcounty_fk', to='cpovc_main.SetupGeography', null=True),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='children_office',
            field=models.ForeignKey(related_name='children_office_fk', to='cpovc_registry.RegOrgUnit', null=True),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='fostered_from',
            field=models.ForeignKey(related_name='fostered_from_fk', to='cpovc_registry.RegOrgUnit', null=True),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='residential_institution_name',
            field=models.ForeignKey(related_name='residential_institution_name_fk', to='cpovc_registry.RegOrgUnit', null=True),
        ),
        migrations.AddField(
            model_name='ovceducationlevelfollowup',
            name='education_followup_id',
            field=models.ForeignKey(to='cpovc_forms.OVCEducationFollowUp'),
        ),
        migrations.AddField(
            model_name='ovceducationfollowup',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovceducationfollowup',
            name='placement_id',
            field=models.ForeignKey(to='cpovc_forms.OVCPlacement', null=True),
        ),
        migrations.AddField(
            model_name='ovceducationfollowup',
            name='school_id',
            field=models.ForeignKey(to='cpovc_main.SchoolList', null=True),
        ),
        migrations.AddField(
            model_name='ovceconomicstatus',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovceconomicstatus',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcdocuments',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcdischargefollowup',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcdischargefollowup',
            name='placement_id',
            field=models.ForeignKey(to='cpovc_forms.OVCPlacement'),
        ),
        migrations.AddField(
            model_name='ovccasesubcategory',
            name='case_category',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseCategory'),
        ),
        migrations.AddField(
            model_name='ovccasesubcategory',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccaserecord',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='occurence_county',
            field=models.ForeignKey(related_name='occurence_county_fk', to='cpovc_main.SetupGeography'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='occurence_subcounty',
            field=models.ForeignKey(related_name='occurence_subcounty_fk', to='cpovc_main.SetupGeography'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='report_orgunit',
            field=models.ForeignKey(to='cpovc_registry.RegOrgUnit', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='report_subcounty',
            field=models.ForeignKey(related_name='report_subcounty_fk', to='cpovc_main.SetupGeography'),
        ),
        migrations.AddField(
            model_name='ovccaseeventsummon',
            name='case_category',
            field=models.ForeignKey(default=uuid.uuid1, editable=False, to='cpovc_forms.OVCCaseCategory', null=True),
        ),
        migrations.AddField(
            model_name='ovccaseeventsummon',
            name='case_event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseEvents'),
        ),
        migrations.AddField(
            model_name='ovccaseeventservices',
            name='case_category',
            field=models.ForeignKey(default=uuid.uuid1, blank=True, editable=False, to='cpovc_forms.OVCCaseCategory'),
        ),
        migrations.AddField(
            model_name='ovccaseeventservices',
            name='case_event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseEvents'),
        ),
        migrations.AddField(
            model_name='ovccaseevents',
            name='app_user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ovccaseevents',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord', null=True),
        ),
        migrations.AddField(
            model_name='ovccaseevents',
            name='placement_id',
            field=models.ForeignKey(to='cpovc_forms.OVCPlacement', null=True),
        ),
        migrations.AddField(
            model_name='ovccaseeventcourt',
            name='case_category',
            field=models.ForeignKey(default=uuid.uuid1, blank=True, editable=False, to='cpovc_forms.OVCCaseCategory'),
        ),
        migrations.AddField(
            model_name='ovccaseeventcourt',
            name='case_event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseEvents'),
        ),
        migrations.AddField(
            model_name='ovccaseeventclosure',
            name='case_event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseEvents'),
        ),
        migrations.AddField(
            model_name='ovccaseeventclosure',
            name='transfer_to',
            field=models.ForeignKey(to='cpovc_registry.RegOrgUnit', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='ovccasecategory',
            name='case_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ovccasecategory',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccareservices',
            name='event',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovccarepriority',
            name='event',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovccaref1b',
            name='event',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovccareevents',
            name='house_hold',
            field=models.ForeignKey(to='cpovc_ovc.OVCHouseHold', null=True),
        ),
        migrations.AddField(
            model_name='ovccareevents',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson', null=True),
        ),
        migrations.AddField(
            model_name='ovccareeav',
            name='event',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovccareassessment',
            name='event',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovcbursary',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcadverseeventsotherfollowup',
            name='adverse_condition_id',
            field=models.ForeignKey(to='cpovc_forms.OVCAdverseEventsFollowUp'),
        ),
        migrations.AddField(
            model_name='ovcadverseeventsfollowup',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcadverseeventsfollowup',
            name='placement_id',
            field=models.ForeignKey(to='cpovc_forms.OVCPlacement'),
        ),
        migrations.AddField(
            model_name='formslog',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson', null=True),
        ),
        migrations.AddField(
            model_name='formsaudittrail',
            name='app_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
