# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0026_auto_20190715_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ovchivmanagement',
            name='substitution_firstline_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 9, 16, 53, 158211)),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 9, 16, 53, 157273), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 9, 16, 53, 157246), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 7, 15, 9, 16, 53, 157336), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 9, 16, 53, 157164), null=True),
        ),
    ]
