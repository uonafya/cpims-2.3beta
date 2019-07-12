# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0014_auto_20190711_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ovchivmanagement',
            name='timestamp_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ovchivmanagement',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
