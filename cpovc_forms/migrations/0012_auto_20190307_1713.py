# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0011_auto_20190307_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovcmonitoring',
            name='case_closure_checked',
            field=models.CharField(default=3, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovcmonitoring',
            name='undernourished',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ovcmonitoring',
            name='quarter',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
