# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('role', models.CharField(default=b'Public', max_length=20)),
                ('username', models.CharField(unique=True, max_length=20)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
                ('password_changed_timestamp', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'auth_user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='CPOVCPermission',
            fields=[
                ('permission_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Permission')),
                ('permission_description', models.CharField(max_length=255)),
                ('permission_set', models.CharField(max_length=100)),
                ('permission_type', models.CharField(max_length=50, blank=True)),
                ('restricted_to_self', models.BooleanField(default=False)),
                ('restricted_to_org_unit', models.BooleanField(default=False)),
                ('restricted_to_geo', models.BooleanField(default=False)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'auth_permission_detail',
            },
            bases=('auth.permission',),
        ),
        migrations.CreateModel(
            name='CPOVCRole',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('group_id', models.CharField(max_length=5)),
                ('group_name', models.CharField(max_length=100)),
                ('group_description', models.CharField(max_length=255)),
                ('restricted_to_org_unit', models.BooleanField(default=False)),
                ('restricted_to_geo', models.BooleanField(default=False)),
                ('automatic', models.BooleanField(default=False)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'auth_group_detail',
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='CPOVCUserRoleGeoOrg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'auth_user_groups_geo_org',
            },
        ),
    ]
