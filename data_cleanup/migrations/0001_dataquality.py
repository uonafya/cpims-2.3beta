# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_cleanup', 'data_quality'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataQuality',
            fields=[
                ('ovc_registration_id', models.IntegerField(serialize=False, primary_key=True)),
                ('registration_date', models.DateTimeField()),
                ('has_bcert', models.BooleanField()),
                ('is_disabled', models.BooleanField()),
                ('hiv_status', models.CharField(max_length=255)),
                ('school_level', models.CharField(max_length=255)),
                ('immunization_status', models.CharField(max_length=255)),
                ('org_unique_id', models.CharField(max_length=255)),
                ('exit_reason', models.CharField(max_length=255)),
                ('exit_date', models.CharField(max_length=255)),
                ('ovc_registration_created_at', models.CharField(max_length=255)),
                ('ovc_registration_is_active', models.BooleanField()),
                ('ovc_registration_is_void', models.BooleanField()),
                ('caretaker_id', models.CharField(max_length=255)),
                ('child_cbo_id', models.CharField(max_length=255)),
                ('child_chv_id', models.CharField(max_length=255)),
                ('person_id', models.CharField(max_length=255)),
                ('art_status', models.CharField(max_length=255)),
                ('reg_person_id', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('other_names', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('des_phone_number', models.CharField(max_length=255)),
                ('date_of_birth', models.DateTimeField()),
                ('sex_id', models.CharField(max_length=255)),
                ('is_void', models.BooleanField()),
                ('reg_person_created_at', models.DateTimeField()),
                ('created_by_id', models.IntegerField()),
                ('age', models.IntegerField()),
            ],
            options={
                'db_table': 'data_quality_view',
                'managed': False,
            },
        ),
    ]
