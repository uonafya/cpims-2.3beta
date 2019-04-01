# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0002_auto_20190219_1040'),
        ('cpovc_registry', '0001_initial'),
        ('cpovc_ovc', '0001_initial'),
        ('cpovc_forms', '0002_auto_20190219_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCCareBenchmarkScore',
            fields=[
                ('bench_mark_score_id', models.AutoField(serialize=False, primary_key=True)),
                ('bench_mark_1', models.IntegerField(default=0)),
                ('bench_mark_2', models.IntegerField(default=0)),
                ('bench_mark_3', models.IntegerField(default=0)),
                ('bench_mark_4', models.IntegerField(default=0)),
                ('bench_mark_5', models.IntegerField(default=0)),
                ('bench_mark_6', models.IntegerField(default=0)),
                ('bench_mark_7', models.IntegerField(default=0)),
                ('bench_mark_8', models.IntegerField(default=0)),
                ('bench_mark_9', models.IntegerField(default=0)),
                ('bench_mark_10', models.IntegerField(default=0)),
                ('bench_mark_11', models.IntegerField(default=0)),
                ('bench_mark_12', models.IntegerField(default=0)),
                ('bench_mark_13', models.IntegerField(default=0)),
                ('bench_mark_14', models.IntegerField(default=0)),
                ('bench_mark_15', models.IntegerField(default=0)),
                ('bench_mark_16', models.IntegerField(default=0)),
                ('bench_mark_17', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('is_void', models.BooleanField(default=False)),
                ('date_of_event', models.DateField(default=django.utils.timezone.now)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
                ('care_giver_id', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_care_benchmark_score',
            },
        ),
        migrations.CreateModel(
            name='OVCCareCasePlan',
            fields=[
                ('case_plan_id', models.AutoField(serialize=False, primary_key=True)),
                ('domain', models.CharField(max_length=50)),
                ('goal', models.CharField(max_length=255)),
                ('need', models.CharField(max_length=255)),
                ('priority', models.CharField(max_length=255)),
                ('responsible', models.CharField(max_length=50)),
                ('completion_date', models.DateField(default=django.utils.timezone.now)),
                ('results', models.CharField(max_length=300)),
                ('reasons', models.CharField(max_length=300)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
                ('cp_service_id', models.ForeignKey(to='cpovc_main.SetupList')),
            ],
            options={
                'db_table': 'ovc_care_case_plan',
            },
        ),
        migrations.CreateModel(
            name='OVCCareCpara',
            fields=[
                ('cpara_id', models.AutoField(serialize=False, primary_key=True)),
                ('answer', models.CharField(max_length=5)),
                ('question_type', models.CharField(max_length=50)),
                ('domain', models.CharField(max_length=50)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_care_cpara',
            },
        ),
        migrations.CreateModel(
            name='OVCCareForms',
            fields=[
                ('form_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OVCCareQuestions',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=5)),
                ('question', models.CharField(max_length=255)),
                ('form_id', models.ForeignKey(to='cpovc_forms.OVCCareForms')),
            ],
            options={
                'db_table': 'ovc_care_questions',
            },
        ),
        migrations.CreateModel(
            name='OVCCareWellbeing',
            fields=[
                ('well_being_id', models.AutoField(serialize=False, primary_key=True)),
                ('question', models.CharField(max_length=150)),
                ('answer', models.CharField(max_length=5)),
                ('question_type', models.CharField(max_length=5)),
                ('domain', models.CharField(max_length=10)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ovc_care_well_being',
            },
        ),
        migrations.CreateModel(
            name='OVCExplanations',
            fields=[
                ('explanation_id', models.AutoField(serialize=False, primary_key=True)),
                ('comment', models.CharField(max_length=255)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ovc_explanations',
            },
        ),
        migrations.CreateModel(
            name='OVCGoals',
            fields=[
                ('goal_id', models.AutoField(serialize=False, primary_key=True)),
                ('goal', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ovc_goals',
            },
        ),
        migrations.CreateModel(
            name='OVCHivStatus',
            fields=[
                ('hiv_status_id', models.AutoField(serialize=False, primary_key=True)),
                ('hiv_status', models.CharField(max_length=10)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ovc_hiv_status',
            },
        ),
        migrations.CreateModel(
            name='OVCHouseholdDemographics',
            fields=[
                ('household_demographics_id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=15)),
                ('male', models.IntegerField(default=0)),
                ('female', models.IntegerField(default=0)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ovc_household_demographics',
            },
        ),
        migrations.CreateModel(
            name='OVCMonitoring',
            fields=[
                ('monitoring_id', models.AutoField(serialize=False, primary_key=True)),
                ('hiv_status_knowledge', models.CharField(max_length=5)),
                ('viral_suppression', models.CharField(max_length=5)),
                ('hiv_prevention', models.CharField(max_length=5)),
                ('access_money', models.CharField(max_length=5)),
                ('violence', models.CharField(max_length=5)),
                ('caregiver', models.CharField(max_length=5)),
                ('school_attendance', models.CharField(max_length=5)),
                ('school_progression', models.CharField(max_length=5)),
                ('cp_achievement', models.CharField(max_length=5)),
                ('case_closure', models.CharField(max_length=5)),
                ('is_void', models.BooleanField(default=False)),
                ('event_date', models.DateField(default=django.utils.timezone.now)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ovc_monitoring',
            },
        ),
        migrations.CreateModel(
            name='OVCReferrals',
            fields=[
                ('referral_id', models.AutoField(serialize=False, primary_key=True)),
                ('referral_date', models.DateField(default=django.utils.timezone.now)),
                ('service', models.CharField(max_length=20)),
                ('institution', models.CharField(max_length=50)),
                ('contact_person', models.CharField(max_length=50)),
                ('completed', models.BooleanField(default=False)),
                ('outcome', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ovc_cp_referrals',
            },
        ),
        migrations.AddField(
            model_name='ovccareevents',
            name='date_of_previous_event',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ovcreferrals',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovcreferrals',
            name='person_id',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcmonitoring',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovcmonitoring',
            name='household_id',
            field=models.ForeignKey(to='cpovc_ovc.OVCHouseHold'),
        ),
        migrations.AddField(
            model_name='ovchouseholddemographics',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovchouseholddemographics',
            name='household_id',
            field=models.ForeignKey(to='cpovc_ovc.OVCHouseHold'),
        ),
        migrations.AddField(
            model_name='ovchivstatus',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovchivstatus',
            name='person_id',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcgoals',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovcgoals',
            name='person_id',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcexplanations',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovcexplanations',
            name='form_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareForms'),
        ),
        migrations.AddField(
            model_name='ovcexplanations',
            name='question',
            field=models.ForeignKey(to='cpovc_forms.OVCCareQuestions'),
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='household_id',
            field=models.ForeignKey(to='cpovc_ovc.OVCHouseHold'),
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='person_id',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='household_id',
            field=models.ForeignKey(to='cpovc_ovc.OVCHouseHold'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='person_id',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='question',
            field=models.ForeignKey(to='cpovc_forms.OVCCareQuestions'),
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='form_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareForms'),
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='person_id',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccarebenchmarkscore',
            name='event_id',
            field=models.ForeignKey(to='cpovc_forms.OVCCareEvents'),
        ),
        migrations.AddField(
            model_name='ovccarebenchmarkscore',
            name='household_id',
            field=models.ForeignKey(to='cpovc_ovc.OVCHouseHold'),
        ),
    ]
