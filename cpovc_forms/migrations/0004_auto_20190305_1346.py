# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0003_auto_20190301_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ovccarecaseplan',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='ovccarecaseplan',
            old_name='form_id',
            new_name='form',
        ),
        migrations.RenameField(
            model_name='ovccarequestions',
            old_name='form_id',
            new_name='form',
        ),
        migrations.RenameField(
            model_name='ovcexplanations',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='ovcexplanations',
            old_name='form_id',
            new_name='form',
        ),
        migrations.RenameField(
            model_name='ovcgoals',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='ovcgoals',
            old_name='person_id',
            new_name='person',
        ),
        migrations.RenameField(
            model_name='ovchouseholddemographics',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RemoveField(
            model_name='ovccarecpara',
            name='question',
        ),
        migrations.RemoveField(
            model_name='ovccareforms',
            name='form_id',
        ),
        migrations.RemoveField(
            model_name='ovccarequestions',
            name='question_id',
        ),
        migrations.RemoveField(
            model_name='ovccarewellbeing',
            name='question',
        ),
        migrations.RemoveField(
            model_name='ovcexplanations',
            name='question',
        ),
        migrations.AddField(
            model_name='ovccareforms',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='question_type',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ovchivstatus',
            name='date_1',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterModelTable(
            name='ovccareforms',
            table='ovc_care_forms',
        ),
    ]
