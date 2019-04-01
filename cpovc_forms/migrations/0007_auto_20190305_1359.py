# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0006_auto_20190305_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCCareForms',
            fields=[
                ('form_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ovc_care_forms',
            },
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='form',
            field=models.ForeignKey(to='cpovc_forms.OVCCareForms'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='form',
            field=models.ForeignKey(to='cpovc_forms.OVCCareForms'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovcexplanations',
            name='form',
            field=models.ForeignKey(to='cpovc_forms.OVCCareForms'),
            preserve_default=False,
        ),
    ]
