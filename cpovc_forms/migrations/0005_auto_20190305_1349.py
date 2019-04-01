# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0004_auto_20190305_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ovccareforms',
            name='id',
        ),
        migrations.RemoveField(
            model_name='ovccarequestions',
            name='id',
        ),
        migrations.AddField(
            model_name='ovccareforms',
            name='form_id',
            field=models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='question_id',
            field=models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True),
        ),
    ]
