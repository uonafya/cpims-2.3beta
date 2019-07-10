# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0005_auto_20190403_1021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listanswers',
            old_name='timestamp_modified',
            new_name='timestamp_updated',
        ),
        migrations.RenameField(
            model_name='listquestions',
            old_name='timestamp_modified',
            new_name='timestamp_updated',
        ),
        migrations.RemoveField(
            model_name='setuplist',
            name='timestamp_modified',
        ),
        migrations.AddField(
            model_name='coreencounters',
            name='timestamp_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='coreencounters',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='coreservices',
            name='timestamp_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='coreservices',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='facilitylist',
            name='timestamp_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='facilitylist',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='listanswers',
            name='timestamp_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='listquestions',
            name='timestamp_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='schoollist',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='setuplist',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='forms',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='setupgeography',
            name='timestamp_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='setuplist',
            name='item_description_short',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='setuplist',
            name='item_id',
            field=models.CharField(max_length=7),
        ),
    ]
