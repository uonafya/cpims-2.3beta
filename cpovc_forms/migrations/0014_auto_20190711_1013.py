# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0013_auto_20190711_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 11, 10, 13, 14, 879673), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 11, 10, 13, 14, 879650), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 11, 10, 13, 14, 879589), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='timestamp_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
