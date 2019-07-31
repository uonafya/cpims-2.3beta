# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_cleanup', 'from_1b_migrations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form1BServicesDataQuality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('form_id', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('entity', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('event_id', models.CharField(max_length=255)),
                ('person_id', models.CharField(max_length=255)),
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
            ],
            options={
                'db_table': 'data_quality_form1b',
                'managed': False,
            },
        ),
    ]
