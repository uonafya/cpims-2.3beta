# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0010_auto_20190306_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovccarecpara',
            name='question_code',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='timestamp_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 7, 10, 41, 5, 499174, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='domain',
            field=models.CharField(default='GEN', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='is_void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='question_text',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='timestamp_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='timestamp_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 7, 10, 41, 50, 902996, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='question_code',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AddField(
            model_name='ovcexplanations',
            name='is_void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ovcgoals',
            name='is_void',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ovccarequestions',
            name='question',
            field=models.CharField(max_length=55),
        ),
    ]
