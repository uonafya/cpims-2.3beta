# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_ovc', '0006_auto_20190710_1201'),
        ('cpovc_registry', '0002_auto_20180712_1945'),
        ('cpovc_forms', '0008_ovccarecpara_caregiver'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCHIVManagement',
            fields=[
                ('adherence_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('Hiv_Confirmed_Date', models.DateTimeField()),
                ('Treatment_initiated_Date', models.DateTimeField()),
                ('FirstLine_Start_Date', models.DateTimeField()),
                ('Substitution_FirstLine_ARV', models.BooleanField(default=False)),
                ('Substitution_FirstLine_Date', models.DateTimeField()),
                ('Switch_SecondLine_ARV', models.BooleanField(default=False)),
                ('Switch_SecondLine_Date', models.DateTimeField()),
                ('Switch_ThirdLine_ARV', models.BooleanField(default=False)),
                ('Switch_ThirdLine_Date', models.DateTimeField()),
                ('Visit_Date', models.DateTimeField()),
                ('Duration_ART', models.CharField(max_length=6)),
                ('Height', models.CharField(max_length=6)),
                ('MUAC', models.CharField(max_length=20)),
                ('Adherence', models.CharField(max_length=20)),
                ('Adherence_Drugs_Duration', models.CharField(max_length=6)),
                ('Adherence_counselling', models.CharField(max_length=20)),
                ('Treatment_Supporter_Relationship', models.CharField(max_length=20)),
                ('Treatment_Supporter_Gender', models.BooleanField(default=False)),
                ('Treatment_Supporter_Age', models.CharField(max_length=6)),
                ('Treament_Supporter_HIV', models.CharField(max_length=10)),
                ('Viral_Load_Results', models.CharField(max_length=6)),
                ('Viral_Load_Date', models.DateTimeField()),
                ('Detectable_ViralLoad_Interventions', models.CharField(max_length=50)),
                ('Disclosure', models.CharField(max_length=20)),
                ('MUAC_Score', models.CharField(max_length=20)),
                ('BMI', models.CharField(max_length=20)),
                ('Nutritional_Support', models.CharField(max_length=50)),
                ('Support_group_Enrollment', models.BooleanField(default=False)),
                ('Support_group_Status', models.BooleanField(default=False)),
                ('NHIF_Enrollment', models.BooleanField(default=False)),
                ('NHIF_Status', models.BooleanField(default=False)),
                ('Referral_Services', models.CharField(max_length=100)),
                ('NextAppointment_Date', models.DateField()),
                ('Peer_Educator_Name', models.CharField(max_length=100)),
                ('Peer_Educator_Contact', models.CharField(max_length=20)),
                ('is_void', models.BooleanField(default=False)),
                ('date_of_event', models.DateField()),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(to='cpovc_forms.OVCCareEvents')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_hiv_management',
            },
        ),
        migrations.CreateModel(
            name='OVCHIVRiskScreening',
            fields=[
                ('risk_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('test_done_when', models.BooleanField(default=False)),
                ('test_donewhen_result', models.BooleanField(default=False)),
                ('caregiver_know_status', models.BooleanField()),
                ('caregiver_knowledge_yes', models.CharField(max_length=50)),
                ('parent_PLWH', models.BooleanField(default=False)),
                ('child_sick_malnourished', models.BooleanField(default=False)),
                ('child_sexual_abuse', models.BooleanField(default=False)),
                ('adol_sick', models.BooleanField(default=False)),
                ('adol_sexual_abuse', models.BooleanField(default=False)),
                ('sex', models.BooleanField(default=False)),
                ('sti', models.BooleanField(default=False)),
                ('hiv_test_required', models.BooleanField(default=False)),
                ('parent_consent_testing', models.BooleanField(default=False)),
                ('referral_made', models.BooleanField(default=False)),
                ('referral_made_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('referral_completed', models.BooleanField(default=False)),
                ('not_completed', models.CharField(max_length=50)),
                ('test_result', models.CharField(max_length=20)),
                ('art_referral', models.BooleanField(default=False)),
                ('art_referral_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('art_referral_completed', models.BooleanField(default=False)),
                ('art_referral_completed_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('date_of_event', models.DateField()),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(to='cpovc_forms.OVCCareEvents')),
                ('facility', models.ForeignKey(to='cpovc_ovc.OVCFacility')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_risk_screening',
            },
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='actual_completion_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ovccareassessment',
            name='service_status',
            field=models.CharField(max_length=7),
        ),
    ]
