# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0002_auto_20180419_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setuplist',
            name='item_description_short',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
