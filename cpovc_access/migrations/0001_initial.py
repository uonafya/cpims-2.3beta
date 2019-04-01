# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_agent', models.CharField(max_length=255)),
                ('ip_address', models.GenericIPAddressField(null=True, verbose_name=b'IP Address')),
                ('username', models.CharField(max_length=255, null=True)),
                ('trusted', models.BooleanField(default=False)),
                ('http_accept', models.CharField(max_length=1025, verbose_name=b'HTTP Accept')),
                ('path_info', models.CharField(max_length=255, verbose_name=b'Path')),
                ('attempt_time', models.DateTimeField(auto_now_add=True)),
                ('get_data', models.TextField(verbose_name=b'GET Data')),
                ('post_data', models.TextField(verbose_name=b'POST Data')),
                ('failures_since_start', models.PositiveIntegerField(verbose_name=b'Failed Logins')),
            ],
            options={
                'db_table': 'auth_login_attempt',
            },
        ),
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_agent', models.CharField(max_length=255)),
                ('ip_address', models.GenericIPAddressField(null=True, verbose_name=b'IP Address')),
                ('username', models.CharField(max_length=255, null=True)),
                ('trusted', models.BooleanField(default=False)),
                ('http_accept', models.CharField(max_length=1025, verbose_name=b'HTTP Accept')),
                ('path_info', models.CharField(max_length=255, verbose_name=b'Path')),
                ('attempt_time', models.DateTimeField(auto_now_add=True)),
                ('logout_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'auth_login_accesslog',
            },
        ),
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('names', models.CharField(max_length=100)),
                ('email_address', models.EmailField(unique=True, max_length=100)),
                ('phone_number', models.CharField(unique=True, max_length=20)),
                ('ip_address', models.GenericIPAddressField()),
                ('timestamp_requested', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'auth_login_request',
            },
        ),
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100, verbose_name='username', db_index=True)),
                ('source_address', models.GenericIPAddressField(verbose_name='source address', db_index=True)),
                ('hostname', models.CharField(max_length=100, verbose_name='hostname')),
                ('successful', models.BooleanField(default=False, verbose_name='successful')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp', db_index=True)),
                ('user_repr', models.CharField(max_length=200, verbose_name='user', blank=True)),
                ('lockout', models.BooleanField(default=True, help_text='Counts towards lockout count', verbose_name='lockout')),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'auth_login_policy',
                'verbose_name': 'login attempt',
                'verbose_name_plural': 'login attempts',
                'permissions': (('unlock', 'Unlock by username or IP address'),),
            },
        ),
        migrations.CreateModel(
            name='PasswordChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_repr', models.CharField(max_length=200, verbose_name='user')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('successful', models.BooleanField(default=False, verbose_name='successful')),
                ('is_temporary', models.BooleanField(default=False, verbose_name='is temporary')),
                ('password', models.CharField(default=b'', verbose_name='password', max_length=128, editable=False)),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'auth_password_history',
                'verbose_name': 'password change',
                'verbose_name_plural': 'password changes',
            },
        ),
        migrations.CreateModel(
            name='UserChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_repr', models.CharField(max_length=200, verbose_name='user')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('by_user_repr', models.CharField(max_length=200, verbose_name='by user')),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'auth_user_history',
                'verbose_name': 'user change',
                'verbose_name_plural': 'user changes',
            },
        ),
    ]
