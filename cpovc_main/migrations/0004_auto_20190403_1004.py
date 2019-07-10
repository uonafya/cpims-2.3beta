# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0003_auto_20180912_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setuplist',
            name='item_description_short',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
