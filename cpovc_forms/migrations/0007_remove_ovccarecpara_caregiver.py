# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0006_auto_20190422_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ovccarecpara',
            name='caregiver',
        ),
    ]
