# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0002_auto_20180712_1945'),
        ('cpovc_forms', '0007_remove_ovccarecpara_caregiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovccarecpara',
            name='caregiver',
            field=models.ForeignKey(related_name='cpara_caregiver', default=1, to='cpovc_registry.RegPerson'),
            preserve_default=False,
        ),
    ]
