# -*- coding: utf-8 -*-
import os
from django.db import models, migrations

with open(os.path.dirname(os.path.realpath(__file__))+'/../sql/form1b_migrations.sql') as f:
   sql = f.read()

class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', 'data_quality'),
    ]

    operations = [
        migrations.RunSQL(sql),
    ]