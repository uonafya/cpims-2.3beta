# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0004_auto_20190403_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setuplist',
            name='item_description_short',
            field=models.CharField(max_length=26, null=True),
        ),
    ]
