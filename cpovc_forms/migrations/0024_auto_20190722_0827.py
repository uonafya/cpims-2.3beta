# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0023_auto_20190719_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ovccarewellbeing',
            name='caregiver',
        ),
        migrations.AlterField(
            model_name='ovccarewellbeing',
            name='domain',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ovchivmanagement',
            name='substitution_firstline_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 22, 8, 27, 41, 455975)),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 22, 8, 27, 41, 455147), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 22, 8, 27, 41, 455127), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 7, 22, 8, 27, 41, 455202), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 22, 8, 27, 41, 455050), null=True),
        ),
    ]
