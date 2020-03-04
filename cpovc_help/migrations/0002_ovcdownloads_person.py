# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_help', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovcdownloads',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson', null=True),
        ),
    ]
