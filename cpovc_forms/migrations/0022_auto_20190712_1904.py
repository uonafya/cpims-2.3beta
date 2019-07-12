# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0021_auto_20190712_1506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Adherence',
            new_name='adherence',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Peer_Educator_Name',
            new_name='baseline_hei',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='FirstLine_Start_Date',
            new_name='firstline_start_date',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Hiv_Confirmed_Date',
            new_name='hiv_confirmed_date',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='NHIF_Enrollment',
            new_name='nhif_enrollment',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='NHIF_Status',
            new_name='switch_secondline_arv',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Support_group_Status',
            new_name='switch_thirdline_arv',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Substitution_FirstLine_Date',
            new_name='treatment_initiated_date',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Switch_SecondLine_Date',
            new_name='viral_load_date',
        ),
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Switch_ThirdLine_Date',
            new_name='visit_date',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Adherence_Drugs_Duration',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Adherence_counselling',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='BMI',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Detectable_ViralLoad_Interventions',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Disclosure',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Duration_ART',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Height',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='MUAC',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='MUAC_Score',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='NextAppointment_Date',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Nutritional_Support',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Peer_Educator_Contact',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Referral_Services',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Switch_SecondLine_ARV',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Switch_ThirdLine_ARV',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Treament_Supporter_HIV',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Treatment_Supporter_Age',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Treatment_Supporter_Gender',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Treatment_Supporter_Relationship',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Treatment_initiated_Date',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Viral_Load_Date',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Viral_Load_Results',
        ),
        migrations.RemoveField(
            model_name='ovchivmanagement',
            name='Visit_Date',
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='adherence_counselling',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='adherence_drugs_duration',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='bmi',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='detectable_viralload_interventions',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='disclosure',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='duration_art',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='height',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='muac',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='muac_score',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='nextappointment_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='nhif_status',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='nutritional_support',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='peer_educator_contact',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='peer_educator_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='referral_services',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='substitution_firstline_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 12, 19, 4, 23, 561430)),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='support_group_status',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='switch_secondline_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='switch_thirdline_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='treament_supporter_hiv',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='treatment_supporter_age',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='treatment_supporter_gender',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='treatment_supporter_relationship',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='treatment_suppoter',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='viral_load_results',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 12, 19, 4, 23, 557898), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 12, 19, 4, 23, 557833), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 7, 12, 19, 4, 23, 558119), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 12, 19, 4, 23, 557588), null=True),
        ),
    ]
