# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_main', '0002_auto_20180419_1202'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCAggregate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator_name', models.CharField(max_length=100)),
                ('project_year', models.IntegerField()),
                ('reporting_period', models.CharField(max_length=50)),
                ('cbo', models.CharField(max_length=255)),
                ('subcounty', models.CharField(max_length=100)),
                ('county', models.CharField(max_length=100)),
                ('ward', models.CharField(max_length=100)),
                ('implementing_partnerid', models.IntegerField()),
                ('implementing_partner', models.CharField(max_length=200)),
                ('indicator_count', models.IntegerField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=50)),
                ('county_active', models.IntegerField()),
                ('subcounty_active', models.IntegerField()),
                ('ward_active', models.IntegerField()),
                ('created_at', models.DateField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'ovc_aggregate',
                'verbose_name': 'OVC aggregate data',
                'verbose_name_plural': 'OVC aggregate data',
            },
        ),
        migrations.CreateModel(
            name='OVCCluster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('cluster_name', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ovc_cluster',
                'verbose_name': 'OVC Cluster',
                'verbose_name_plural': 'OVC Clusters',
            },
        ),
        migrations.CreateModel(
            name='OVCClusterCBO',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('cbo', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
                ('cluster', models.ForeignKey(to='cpovc_ovc.OVCCluster')),
            ],
            options={
                'db_table': 'ovc_cluster_cbo',
                'verbose_name': 'OVC Cluster CBO',
                'verbose_name_plural': 'OVC Cluster CBOs',
            },
        ),
        migrations.CreateModel(
            name='OVCEducation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('school_level', models.CharField(max_length=4)),
                ('school_class', models.CharField(max_length=4)),
                ('admission_type', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_care_education',
                'verbose_name': 'OVC Care Education',
                'verbose_name_plural': 'OVC Care Education',
            },
        ),
        migrations.CreateModel(
            name='OVCEligibility',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('criteria', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_eligibility',
                'verbose_name': 'OVC Eligibility',
                'verbose_name_plural': 'OVC Eligibility',
            },
        ),
        migrations.CreateModel(
            name='OVCFacility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facility_code', models.CharField(max_length=10, null=True)),
                ('facility_name', models.CharField(max_length=200)),
                ('is_void', models.BooleanField(default=False)),
                ('sub_county', models.ForeignKey(to='cpovc_main.SetupGeography', null=True)),
            ],
            options={
                'db_table': 'ovc_facility',
                'verbose_name': 'OVC Facility',
                'verbose_name_plural': 'OVC Facilities',
            },
        ),
        migrations.CreateModel(
            name='OVCHealth',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('art_status', models.CharField(max_length=4)),
                ('date_linked', models.DateField()),
                ('ccc_number', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('facility', models.ForeignKey(to='cpovc_ovc.OVCFacility')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_care_health',
                'verbose_name': 'OVC Care Health',
                'verbose_name_plural': 'OVC Care Health',
            },
        ),
        migrations.CreateModel(
            name='OVCHHMembers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('hh_head', models.BooleanField(default=False)),
                ('member_type', models.CharField(max_length=4)),
                ('member_alive', models.CharField(default=b'AYES', max_length=4)),
                ('death_cause', models.CharField(max_length=4, null=True)),
                ('hiv_status', models.CharField(max_length=4, null=True)),
                ('date_linked', models.DateField(default=django.utils.timezone.now)),
                ('date_delinked', models.DateField(null=True)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_household_members',
                'verbose_name': 'OVC Registration',
                'verbose_name_plural': 'OVC Registration',
            },
        ),
        migrations.CreateModel(
            name='OVCHouseHold',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('head_identifier', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('head_person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_household',
                'verbose_name': 'OVC Registration',
                'verbose_name_plural': 'OVC Registration',
            },
        ),
        migrations.CreateModel(
            name='OVCRegistration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('registration_date', models.DateField(default=django.utils.timezone.now)),
                ('has_bcert', models.BooleanField(default=False)),
                ('is_disabled', models.BooleanField(default=False)),
                ('hiv_status', models.CharField(max_length=4, null=True)),
                ('art_status', models.CharField(max_length=4, null=True)),
                ('school_level', models.CharField(max_length=4, null=True)),
                ('immunization_status', models.CharField(max_length=4, null=True)),
                ('org_unique_id', models.CharField(max_length=15, null=True)),
                ('exit_reason', models.CharField(max_length=4, null=True)),
                ('exit_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('is_void', models.BooleanField(default=False)),
                ('caretaker', models.ForeignKey(related_name='ctaker', to='cpovc_registry.RegPerson', null=True)),
                ('child_cbo', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
                ('child_chv', models.ForeignKey(related_name='chv', to='cpovc_registry.RegPerson')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_registration',
                'verbose_name': 'OVC Registration',
                'verbose_name_plural': 'OVC Registration',
            },
        ),
        migrations.CreateModel(
            name='OVCSchool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('school_level', models.CharField(default=b'1', max_length=5, choices=[(b'SLEC', b'ECD'), (b'SLPR', b'Primary'), (b'SLSE', b'Secondary'), (b'SLUN', b'University'), (b'SLTV', b'Tertiary / Vocational')])),
                ('school_name', models.CharField(max_length=200)),
                ('is_void', models.BooleanField(default=False)),
                ('sub_county', models.ForeignKey(to='cpovc_main.SetupGeography')),
            ],
            options={
                'db_table': 'ovc_school',
                'verbose_name': 'OVC school',
                'verbose_name_plural': 'OVC Schools',
            },
        ),
        migrations.CreateModel(
            name='OVCUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('implementing_partnerid', models.IntegerField()),
                ('project_year', models.IntegerField()),
                ('reporting_period', models.CharField(max_length=50)),
                ('ovc_filename', models.CharField(max_length=255)),
                ('created_at', models.DateField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'ovc_upload',
                'verbose_name': 'OVC upload data',
                'verbose_name_plural': 'OVC upload data',
            },
        ),
        migrations.AddField(
            model_name='ovchhmembers',
            name='house_hold',
            field=models.ForeignKey(default=uuid.uuid4, to='cpovc_ovc.OVCHouseHold'),
        ),
        migrations.AddField(
            model_name='ovchhmembers',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovceducation',
            name='school',
            field=models.ForeignKey(to='cpovc_ovc.OVCSchool'),
        ),
    ]
