# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0010_auto_20190711_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='adol_sexual_abuse',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='adol_sick',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='caregiver_knowledge_yes',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='child_sexual_abuse',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='child_sick_malnourished',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='hiv_test_required',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='is_void',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='parent_PLWH',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='parent_consent_testing',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_completed',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='sex',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='sti',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='test_done_when',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='test_donewhen_result',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='test_result',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
