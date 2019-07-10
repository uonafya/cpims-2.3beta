# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_ovc', '0003_ovcregistration_art_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCExit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('org_unit_name', models.CharField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit', null=True)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_exit_organization',
                'verbose_name': 'OVC Exit Org Unit',
                'verbose_name_plural': 'OVC Exit Org Units',
            },
        ),
    ]
