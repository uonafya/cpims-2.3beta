# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCaptureSites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_unit_id', models.IntegerField(null=True)),
                ('capture_site_name', models.CharField(max_length=255, null=True, blank=True)),
                ('date_installed', models.DateField(null=True, blank=True)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'admin_capture_sites',
            },
        ),
        migrations.CreateModel(
            name='AdminDownload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capture_site_id', models.IntegerField(null=True, blank=True)),
                ('section_id', models.CharField(max_length=4, null=True)),
                ('timestamp_started', models.DateTimeField(null=True)),
                ('timestamp_completed', models.DateTimeField(null=True)),
                ('number_records', models.IntegerField(null=True)),
                ('request_id', models.CharField(max_length=64, null=True)),
                ('success', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'admin_download',
            },
        ),
        migrations.CreateModel(
            name='AdminPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preference_id', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'admin_preferences',
            },
        ),
        migrations.CreateModel(
            name='AdminUploadForms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp_uploaded', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'admin_upload_forms',
            },
        ),
        migrations.CreateModel(
            name='CaptureTaskTracker',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('task_id', models.CharField(max_length=64, null=True)),
                ('operation', models.CharField(max_length=8, null=True)),
                ('timestamp_started', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_completed', models.DateTimeField(null=True)),
                ('completed', models.BooleanField(default=False)),
                ('cancelled', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'admin_task_tracker',
            },
        ),
        migrations.CreateModel(
            name='CoreAdverseConditions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adverse_condition_id', models.CharField(max_length=4)),
                ('is_void', models.BooleanField(default=False)),
                ('sms_id', models.IntegerField(null=True)),
                ('form_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'core_adverse_conditions',
            },
        ),
        migrations.CreateModel(
            name='CoreEncounters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('encounter_date', models.DateField()),
                ('org_unit_id', models.IntegerField()),
                ('area_id', models.IntegerField()),
                ('encounter_type_id', models.CharField(max_length=4)),
                ('sms_id', models.IntegerField(null=True)),
                ('form_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'core_encounters',
            },
        ),
        migrations.CreateModel(
            name='CoreEncountersNotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('form_id', models.IntegerField()),
                ('encounter_date', models.DateField()),
                ('note_type_id', models.CharField(max_length=4)),
                ('note', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'form_encounters_notes',
            },
        ),
        migrations.CreateModel(
            name='CoreServices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('encounter_date', models.DateField()),
                ('core_item_id', models.CharField(max_length=4)),
                ('sms_id', models.IntegerField(null=True)),
                ('form_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'core_services',
            },
        ),
        migrations.CreateModel(
            name='FacilityList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facility_code', models.IntegerField()),
                ('facility_name', models.CharField(max_length=255)),
                ('county_id', models.IntegerField()),
                ('county_name', models.CharField(max_length=255)),
                ('subcounty_id', models.IntegerField()),
                ('subcounty_name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=5)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=5)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'facility_list',
            },
        ),
        migrations.CreateModel(
            name='FormGenAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'form_gen_answers',
            },
        ),
        migrations.CreateModel(
            name='FormGenDates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_date', models.DateField()),
            ],
            options={
                'db_table': 'form_gen_dates',
            },
        ),
        migrations.CreateModel(
            name='FormGenNumeric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.DecimalField(null=True, max_digits=10, decimal_places=1)),
            ],
            options={
                'db_table': 'form_gen_numeric',
            },
        ),
        migrations.CreateModel(
            name='FormGenText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'form_gen_text',
            },
        ),
        migrations.CreateModel(
            name='FormOrgUnitContributions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_unit_id', models.CharField(max_length=7)),
                ('contribution_id', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'form_org_unit_contribution',
            },
        ),
        migrations.CreateModel(
            name='FormPersonParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('workforce_or_beneficiary_id', models.CharField(max_length=15)),
                ('participation_level_id', models.CharField(max_length=4, null=True, blank=True)),
            ],
            options={
                'db_table': 'form_person_participation',
            },
        ),
        migrations.CreateModel(
            name='FormResChildren',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child_person_id', models.IntegerField(null=True, blank=True)),
                ('institution_id', models.IntegerField(null=True, blank=True)),
                ('residential_status_id', models.CharField(max_length=4, null=True, blank=True)),
                ('court_committal_id', models.CharField(max_length=4, null=True, blank=True)),
                ('family_status_id', models.CharField(max_length=4, null=True, blank=True)),
                ('date_admitted', models.DateField(null=True, blank=True)),
                ('date_left', models.DateField(null=True, blank=True)),
                ('sms_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'form_res_children',
            },
        ),
        migrations.CreateModel(
            name='FormResWorkforce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('workforce_id', models.IntegerField(null=True, blank=True)),
                ('institution_id', models.IntegerField(null=True, blank=True)),
                ('position_id', models.CharField(max_length=4, null=True, blank=True)),
                ('full_part_time_id', models.CharField(max_length=4, null=True, blank=True)),
            ],
            options={
                'db_table': 'form_res_workforce',
            },
        ),
        migrations.CreateModel(
            name='Forms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('form_guid', models.CharField(max_length=64)),
                ('form_title', models.CharField(max_length=255, null=True)),
                ('form_type_id', models.CharField(max_length=4, null=True)),
                ('form_subject_id', models.IntegerField(null=True)),
                ('form_area_id', models.IntegerField(null=True)),
                ('date_began', models.DateField(null=True)),
                ('date_ended', models.DateField(null=True)),
                ('date_filled_paper', models.DateField(null=True)),
                ('person_id_filled_paper', models.IntegerField(null=True)),
                ('org_unit_id_filled_paper', models.IntegerField(null=True)),
                ('capture_site_id', models.IntegerField(null=True, blank=True)),
                ('timestamp_created', models.DateTimeField(null=True)),
                ('user_id_created', models.CharField(max_length=9, null=True)),
                ('timestamp_updated', models.DateTimeField(null=True)),
                ('user_id_updated', models.CharField(max_length=9, null=True)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'forms',
            },
        ),
        migrations.CreateModel(
            name='ListAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_set_id', models.IntegerField(null=True, db_index=True)),
                ('answer', models.CharField(max_length=255, null=True, blank=True)),
                ('the_order', models.IntegerField(null=True, db_index=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True, null=True)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'list_answers',
            },
        ),
        migrations.CreateModel(
            name='ListQuestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=255, null=True, blank=True)),
                ('question_code', models.CharField(max_length=50)),
                ('form_type_id', models.CharField(max_length=4, null=True, blank=True)),
                ('answer_type_id', models.CharField(max_length=4, null=True, blank=True)),
                ('answer_set_id', models.IntegerField(null=True, db_index=True)),
                ('the_order', models.IntegerField(null=True, db_index=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True, null=True)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'list_questions',
            },
        ),
        migrations.CreateModel(
            name='ListReports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_code', models.CharField(max_length=100, null=True, blank=True)),
                ('report_title_short', models.CharField(max_length=255, null=True)),
                ('report_title_long', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'list_reports',
            },
        ),
        migrations.CreateModel(
            name='ListReportsParameters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameter', models.CharField(max_length=50, null=True, blank=True)),
                ('filter', models.CharField(max_length=50, null=True, blank=True)),
                ('initially_visible', models.BooleanField(default=False)),
                ('label', models.CharField(max_length=100, null=True, blank=True)),
                ('tip', models.CharField(max_length=255, null=True, blank=True)),
                ('required', models.BooleanField(default=False)),
                ('report', models.ForeignKey(to='cpovc_main.ListReports', null=True)),
            ],
            options={
                'db_table': 'list_reports_parameter',
            },
        ),
        migrations.CreateModel(
            name='RegTemp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('page_id', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('_data', models.TextField(db_column=b'page_data', blank=True)),
            ],
            options={
                'db_table': 'reg_temp_data',
            },
        ),
        migrations.CreateModel(
            name='ReportsSets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set_name', models.CharField(max_length=70)),
                ('set_type_id', models.CharField(default=b'SORG', max_length=4)),
                ('user_id_created', models.IntegerField()),
            ],
            options={
                'db_table': 'reports_sets',
            },
        ),
        migrations.CreateModel(
            name='ReportsSetsOrgUnits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_unit_id', models.IntegerField()),
                ('set', models.ForeignKey(to='cpovc_main.ReportsSets')),
            ],
            options={
                'db_table': 'reports_sets_org_unit',
            },
        ),
        migrations.CreateModel(
            name='SchoolList',
            fields=[
                ('school_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('school_name', models.CharField(max_length=255)),
                ('type_of_school', models.CharField(max_length=26, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('created_by', models.IntegerField(default=404, null=True)),
            ],
            options={
                'db_table': 'school_list',
            },
        ),
        migrations.CreateModel(
            name='SetupGeography',
            fields=[
                ('area_id', models.IntegerField(serialize=False, primary_key=True)),
                ('area_type_id', models.CharField(max_length=50)),
                ('area_name', models.CharField(max_length=100)),
                ('area_code', models.CharField(max_length=10, null=True)),
                ('parent_area_id', models.IntegerField(null=True)),
                ('area_name_abbr', models.CharField(max_length=5, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'list_geo',
                'verbose_name': 'Setup Geography',
                'verbose_name_plural': 'Setup Geographies',
            },
        ),
        migrations.CreateModel(
            name='SetupList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_id', models.CharField(max_length=4)),
                ('item_description', models.CharField(max_length=255)),
                ('item_description_short', models.CharField(max_length=26, null=True)),
                ('item_category', models.CharField(max_length=255, null=True, blank=True)),
                ('item_sub_category', models.CharField(max_length=255, null=True, blank=True)),
                ('the_order', models.IntegerField(null=True)),
                ('user_configurable', models.BooleanField(default=False)),
                ('sms_keyword', models.BooleanField(default=False)),
                ('is_void', models.BooleanField(default=False)),
                ('field_name', models.CharField(max_length=200, null=True, blank=True)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'list_general',
            },
        ),
        migrations.AddField(
            model_name='schoollist',
            name='school_subcounty',
            field=models.ForeignKey(related_name='school_subcounty_fk', to='cpovc_main.SetupGeography'),
        ),
        migrations.AddField(
            model_name='schoollist',
            name='school_ward',
            field=models.ForeignKey(related_name='school_ward_fk', to='cpovc_main.SetupGeography'),
        ),
        migrations.AddField(
            model_name='formresworkforce',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms'),
        ),
        migrations.AddField(
            model_name='formreschildren',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms', null=True),
        ),
        migrations.AddField(
            model_name='formpersonparticipation',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms'),
        ),
        migrations.AddField(
            model_name='formorgunitcontributions',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms'),
        ),
        migrations.AddField(
            model_name='formgentext',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms'),
        ),
        migrations.AddField(
            model_name='formgentext',
            name='question',
            field=models.ForeignKey(to='cpovc_main.ListQuestions'),
        ),
        migrations.AddField(
            model_name='formgennumeric',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms'),
        ),
        migrations.AddField(
            model_name='formgennumeric',
            name='question',
            field=models.ForeignKey(to='cpovc_main.ListQuestions'),
        ),
        migrations.AddField(
            model_name='formgendates',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms'),
        ),
        migrations.AddField(
            model_name='formgendates',
            name='question',
            field=models.ForeignKey(to='cpovc_main.ListQuestions'),
        ),
        migrations.AddField(
            model_name='formgenanswers',
            name='answer',
            field=models.ForeignKey(to='cpovc_main.ListAnswers', null=True),
        ),
        migrations.AddField(
            model_name='formgenanswers',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms'),
        ),
        migrations.AddField(
            model_name='formgenanswers',
            name='question',
            field=models.ForeignKey(to='cpovc_main.ListQuestions'),
        ),
    ]
