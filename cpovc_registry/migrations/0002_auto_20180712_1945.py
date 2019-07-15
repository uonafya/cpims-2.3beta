# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='regpersonstypes',
            options={'verbose_name': 'Person Type Registry', 'verbose_name_plural': 'Person Types Registries'},
        ),
    ]
