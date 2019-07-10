# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0002_auto_20180712_1945'),
        ('cpovc_forms', '0004_auto_20190403_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='caregiver',
            field=models.ForeignKey(related_name='caseplan_caregiver', default=1, to='cpovc_registry.RegPerson'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='caregiver',
            field=models.ForeignKey(related_name='wellbeing_caregiver', default=1, to='cpovc_registry.RegPerson'),
            preserve_default=False,
        )
    ]
