# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0009_auto_20190710_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ovchivriskscreening',
            name='facility',
        ),
        migrations.AddField(
            model_name='ovchivriskscreening',
            name='facility_code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
