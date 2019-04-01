# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_ovc', '0002_remove_ovcregistration_art_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovcregistration',
            name='art_status',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
