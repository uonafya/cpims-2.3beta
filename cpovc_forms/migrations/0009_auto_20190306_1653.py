# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0008_auto_20190305_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovccarecpara',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 3, 6, 13, 53, 1, 641675, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 3, 6, 13, 53, 9, 826314, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovcgoals',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 3, 6, 13, 53, 17, 621869, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovchivstatus',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 3, 6, 13, 53, 23, 605165, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovcreferrals',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 3, 6, 13, 53, 30, 234270, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ovcmonitoring',
            name='event_date',
            field=models.DateField(),
        ),
    ]
