# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_cleanup', '0001_form1bservicesdataquality'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCCareServicesDataQuality',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('ovc_care_events_person_id', models.CharField(max_length=255)),
                ('has_bcert', models.BooleanField()),
                ('is_disabled', models.BooleanField()),
                ('hiv_status', models.CharField(max_length=255)),
                ('school_level', models.CharField(max_length=255)),
                ('child_cbo_id', models.CharField(max_length=255)),
                ('art_status', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('other_names', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('service_provided', models.CharField(max_length=255)),
                ('service_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'data_quality_ovc_care_services',
                'managed': False,
            },
        ),
    ]
