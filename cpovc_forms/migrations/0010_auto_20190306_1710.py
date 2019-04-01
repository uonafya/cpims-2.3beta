# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0009_auto_20190306_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ovccarecpara',
            name='answer',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='ovccarewellbeing',
            name='answer',
            field=models.CharField(max_length=15),
        ),
    ]
