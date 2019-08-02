# -*- coding: utf-8 -*-
import os
from django.db import models, migrations

with open(os.path.dirname(os.path.realpath(__file__))+'/../sql/data_quality.sql') as f:
   sql = f.read()

class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0002_auto_20180712_1945'),
    ]

    operations = [
        migrations.RunSQL(sql),
    ]