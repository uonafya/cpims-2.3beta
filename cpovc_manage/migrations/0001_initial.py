# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0002_auto_20200303_1455'),
        ('cpovc_forms', '0003_auto_20200303_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='NOTTChaperon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_void', models.BooleanField(default=False)),
                ('other_person', models.ForeignKey(to='cpovc_forms.OvcCasePersons')),
            ],
            options={
                'db_table': 'nott_chaperon',
                'verbose_name': 'Non Objection to Travel - Chaperon',
                'verbose_name_plural': 'Non Objection to Travel - Chaperons',
            },
        ),
        migrations.CreateModel(
            name='NOTTChild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('returned', models.BooleanField(default=False)),
                ('cleared', models.BooleanField(default=False)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'nott_child',
                'verbose_name': 'Non Objection to Travel - Child',
                'verbose_name_plural': 'Non Objection to Travel - Children',
            },
        ),
        migrations.CreateModel(
            name='NOTTTravel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institution_name', models.CharField(max_length=255)),
                ('country_name', models.CharField(max_length=150)),
                ('travel_date', models.DateField()),
                ('return_date', models.DateField(null=True, blank=True)),
                ('no_applied', models.IntegerField(default=0)),
                ('no_cleared', models.IntegerField(default=0)),
                ('no_returned', models.IntegerField(default=0, null=True, blank=True)),
                ('contacts', models.CharField(max_length=150, null=True, blank=True)),
                ('reason', models.CharField(max_length=150)),
                ('sponsor', models.CharField(max_length=100)),
                ('comments', models.TextField(null=True, blank=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(default=0)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'nott_travel',
                'verbose_name': 'Non Objection to Travel - Travel',
                'verbose_name_plural': 'Non Objection to Travel - Travels',
            },
        ),
        migrations.AddField(
            model_name='nottchild',
            name='travel',
            field=models.ForeignKey(to='cpovc_manage.NOTTTravel'),
        ),
        migrations.AddField(
            model_name='nottchaperon',
            name='travel',
            field=models.ForeignKey(to='cpovc_manage.NOTTTravel'),
        ),
    ]
