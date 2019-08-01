# -*- coding: utf-8 -*-
import os
from django.db import models, migrations

with open(os.path.dirname(os.path.realpath(__file__))+'/../sql/ovc_care_services_quality.sql') as f:
   sql = f.read()

class Migration(migrations.Migration):

    dependencies = [
        ('data_cleanup', '0002_ovccareservicesdataquality'),
    ]

    operations = [
        migrations.RunSQL(sql),
    ]