# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_ovc', '0001_initial'),
        ('cpovc_forms', '0012_auto_20190307_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='case_plan_status',
            field=models.CharField(default=datetime.datetime(2019, 4, 2, 5, 31, 53, 214471, tzinfo=utc), max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='date_of_event',
            field=models.DateField(default=datetime.datetime(2019, 4, 2, 5, 32, 0, 492087, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='household',
            field=models.ForeignKey(default=datetime.datetime(2019, 4, 2, 5, 32, 9, 542826, tzinfo=utc), to='cpovc_ovc.OVCHouseHold'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ovccarebenchmarkscore',
            name='bench_mark_score_id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='ovccarecaseplan',
            name='case_plan_id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='ovccarecpara',
            name='cpara_id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='ovccarewellbeing',
            name='answer',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='ovccarewellbeing',
            name='well_being_id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='ovcexplanations',
            name='explanation_id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='ovcgoals',
            name='goal_id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='ovchouseholddemographics',
            name='household_demographics_id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
    ]
