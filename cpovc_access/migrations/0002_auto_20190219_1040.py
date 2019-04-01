# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_access', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userchange',
            name='by_user',
            field=models.ForeignKey(related_name='changed_users', on_delete=django.db.models.deletion.SET_NULL, verbose_name='by user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='userchange',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='passwordchange',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='loginattempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
