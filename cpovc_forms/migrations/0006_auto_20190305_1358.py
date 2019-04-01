# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0005_auto_20190305_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ovccarecaseplan',
            name='form',
        ),
        migrations.RemoveField(
            model_name='ovccarequestions',
            name='form',
        ),
        migrations.RemoveField(
            model_name='ovcexplanations',
            name='form',
        ),
        migrations.DeleteModel(
            name='OVCCareForms',
        ),
    ]
