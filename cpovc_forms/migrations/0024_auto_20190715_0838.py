# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0023_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Support_group_Enrollment',
            new_name='support_group_enrollment',
        ),
        migrations.AlterField(
            model_name='ovchivmanagement',
            name='substitution_firstline_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 38, 25, 104635)),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 38, 25, 103704), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 38, 25, 103679), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 7, 15, 8, 38, 25, 103767), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 38, 25, 103596), null=True),
        ),
    ]
