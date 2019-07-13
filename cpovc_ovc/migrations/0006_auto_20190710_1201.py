# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_ovc', '0005_ovcviralload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ovcaggregate',
            name='created_at',
        ),
        migrations.AddField(
            model_name='ovcaggregate',
            name='timestamp_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ovcaggregate',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='ovchealth',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=False,
        ),
    ]
