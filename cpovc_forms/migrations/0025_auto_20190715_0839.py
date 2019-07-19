# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0024_auto_20190715_0838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ovchivmanagement',
            old_name='Substitution_FirstLine_ARV',
            new_name='substitution_firstline_arv',
        ),
        migrations.AlterField(
            model_name='ovchivmanagement',
            name='substitution_firstline_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 38, 58, 760945)),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 38, 58, 760014), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 38, 58, 759987), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 7, 15, 8, 38, 58, 760077), null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 15, 8, 38, 58, 759906), null=True),
        ),
    ]
