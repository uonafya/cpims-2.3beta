# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0002_auto_20180712_1945'),
        ('cpovc_ovc', '0004_ovcexit'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCViralload',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('viral_load', models.IntegerField(null=True)),
                ('viral_date', models.DateField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_viral_load',
                'verbose_name': 'OVC Viral Load',
                'verbose_name_plural': 'OVC Viral Loads',
            },
        ),
    ]
