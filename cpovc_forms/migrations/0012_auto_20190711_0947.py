# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0011_auto_20190711_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='test_done_when',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='test_donewhen_result',
            field=models.NullBooleanField(),
        ),
    ]
