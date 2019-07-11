# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0012_auto_20190711_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='adol_sexual_abuse',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='adol_sick',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='art_referral_completed',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='caregiver_know_status',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='child_sexual_abuse',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='child_sick_malnourished',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='hiv_test_required',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='is_void',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='parent_PLWH',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='parent_consent_testing',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_completed',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='referral_made',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='sex',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ovchivriskscreening',
            name='sti',
            field=models.NullBooleanField(),
        ),
    ]
