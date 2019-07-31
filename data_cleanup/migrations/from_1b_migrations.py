# -*- coding: utf-8 -*-
import os
from django.db import models, migrations

with open(os.path.dirname(os.path.realpath(__file__))+'/../sql/form1b_quality.sql') as f:
   sql = f.read()

class Migration(migrations.Migration):

    dependencies = [
        ('data_cleanup', '0001_dataquality'),
    ]

    operations = [
        migrations.RunSQL(sql),
    ]