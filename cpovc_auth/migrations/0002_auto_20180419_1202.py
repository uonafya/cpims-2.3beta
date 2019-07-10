# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_main', '0002_auto_20180419_1202'),
        ('auth', '0006_require_contenttypes_0002'),
        ('cpovc_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpovcuserrolegeoorg',
            name='area',
            field=models.ForeignKey(to='cpovc_main.SetupGeography', null=True),
        ),
        migrations.AddField(
            model_name='cpovcuserrolegeoorg',
            name='group',
            field=models.ForeignKey(to='cpovc_auth.CPOVCRole'),
        ),
        migrations.AddField(
            model_name='cpovcuserrolegeoorg',
            name='org_unit',
            field=models.ForeignKey(to='cpovc_registry.RegOrgUnit', null=True),
        ),
        migrations.AddField(
            model_name='cpovcuserrolegeoorg',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='reg_person',
            field=models.OneToOneField(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
